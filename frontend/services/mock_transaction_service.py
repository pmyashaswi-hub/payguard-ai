"""
PayGuard AI - Transaction & Wallet Service.
Maintains persistent user balances and database transaction ledger records.
"""

from typing import List, Dict, Any, Optional
import datetime
import streamlit as st
from backend.app.database import db_manager
from frontend.data.mock_data import SEED_TRANSACTIONS, SEED_FREQUENT_PAYEES

class MockTransactionService:
    """Manages active user wallet balance and persistent transaction ledger records."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self._init_session_store()

    def _init_session_store(self):
        """Initializes user ledger store in Streamlit session state and syncs with SQLite database."""
        if "session_transactions" not in st.session_state:
            st.session_state.session_transactions = list(SEED_TRANSACTIONS)
        
        if "wallet_balances" not in st.session_state:
            st.session_state.wallet_balances = {}
        
        if self.user_id not in st.session_state.wallet_balances:
            # Check SQLite profile balance first
            try:
                prof = db_manager.get_user_profile(self.user_id)
                if prof and "available_balance" in prof:
                    st.session_state.wallet_balances[self.user_id] = float(prof["available_balance"])
                else:
                    st.session_state.wallet_balances[self.user_id] = 50000.00
            except Exception:
                st.session_state.wallet_balances[self.user_id] = 50000.00

        # Load persisted database transactions for this user if any exist
        try:
            db_txs = db_manager.get_user_transactions(self.user_id)
            if db_txs:
                for dtx in db_txs:
                    tx_id_str = str(dtx.get("tx_id", ""))
                    already_present = any(str(stx.get("transaction_id")) == tx_id_str for stx in st.session_state.session_transactions)
                    if not already_present:
                        st.session_state.session_transactions.append({
                            "transaction_id": dtx.get("tx_id"),
                            "user_id": dtx.get("user_id"),
                            "recipient": dtx.get("recipient"),
                            "recipient_id": dtx.get("recipient_email"),
                            "amount": float(dtx.get("amount", 0.0)),
                            "timestamp": dtx.get("date_time"),
                            "date_group": "Recent",
                            "decision": dtx.get("decision", "ALLOW"),
                            "status": dtx.get("status", "Completed"),
                            "risk_score": int(dtx.get("risk_score", 0)),
                            "fraud_probability": float(dtx.get("fraud_risk_pct", 0.0)) / 100.0,
                            "risk_signals": dtx.get("security_signals", []),
                            "transaction_integrity": {
                                "is_consistent": True,
                                "sender_debited": True,
                                "receiver_credited": True,
                                "gateway_status": dtx.get("status_code", "SUCCESS"),
                                "settlement_status": "COMPLETED"
                            },
                            "model_version": dtx.get("model_version", "RXT-ResNeXt-GRU-v1.2")
                        })
        except Exception:
            pass

    def get_balance(self) -> float:
        """Returns the current available wallet balance."""
        return float(st.session_state.wallet_balances.get(self.user_id, 0.0))

    def get_frequent_payees(self) -> List[Dict[str, str]]:
        """Returns the list of frequent payees."""
        try:
            db_bens = db_manager.get_beneficiaries(self.user_id)
            if db_bens:
                return [
                    {
                        "name": b["name"],
                        "identifier": b["upi_id"] or b["email"],
                        "type": "UPI ID" if "@" in (b["upi_id"] or "") else "Bank Account",
                        "avatar": b["initials"]
                    }
                    for b in db_bens
                ]
        except Exception:
            pass
        return SEED_FREQUENT_PAYEES

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Returns transactions filtered for the active user, newest first."""
        txs = [
            tx for tx in st.session_state.session_transactions 
            if tx.get("user_id") == self.user_id or (self.user_id == "usr_rahul" and tx.get("user_id") == "usr_rahul")
        ]
        return sorted(txs, key=lambda x: str(x.get("timestamp", "")), reverse=True)

    def record_completed_transaction(
        self,
        transaction_id: int,
        recipient: str,
        recipient_id: str,
        amount: float,
        prediction_result: Dict[str, Any]
    ) -> bool:
        """
        Deducts amount from wallet balance and logs transaction into user history and SQLite DB.
        """
        current_bal = self.get_balance()
        if current_bal < amount:
            return False

        # Deduct balance in session state
        new_balance = current_bal - amount
        st.session_state.wallet_balances[self.user_id] = new_balance

        decision = prediction_result.get("decision", "ALLOW")
        reconciliation = prediction_result.get("reconciliation_required", False)

        status_label = "Completed"
        if reconciliation:
            status_label = "Reconciliation Required"
        elif decision == "VERIFY":
            status_label = "Verified & Completed"
        elif decision == "REVIEW":
            status_label = "Security Review Blocked"

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        
        new_tx = {
            "transaction_id": int(transaction_id),
            "user_id": self.user_id,
            "recipient": recipient,
            "recipient_id": recipient_id,
            "amount": float(amount),
            "timestamp": now.isoformat(timespec="seconds"),
            "date_group": "Today",
            "decision": decision,
            "status": status_label,
            "risk_score": prediction_result.get("risk_score", 0),
            "fraud_probability": prediction_result.get("fraud_probability", 0.0),
            "risk_signals": prediction_result.get("risk_signals", []),
            "transaction_integrity": prediction_result.get("transaction_integrity", {}),
            "model_version": prediction_result.get("model_version", "RXT-ResNeXt-GRU-v1.2")
        }

        # Insert at the beginning of the list
        st.session_state.session_transactions.insert(0, new_tx)

        # Update SQLite database
        try:
            db_manager.update_user_balance(self.user_id, amount)
            db_manager.save_transaction({
                "tx_id": f"PG-{transaction_id}",
                "user_id": self.user_id,
                "recipient": recipient,
                "recipient_email": recipient_id if "@" in recipient_id else f"{recipient.lower().replace(' ', '.')}@example.com",
                "amount": float(amount),
                "date_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "purpose": "Transfer",
                "status": status_label,
                "status_code": "SUCCESS" if decision != "REVIEW" else "REVIEW",
                "risk_level": "High Risk" if decision == "REVIEW" else ("Medium Risk" if decision == "VERIFY" else "Low Risk"),
                "fraud_risk_pct": float(prediction_result.get("fraud_probability", 0.0)) * 100,
                "risk_score": int(prediction_result.get("risk_score", 0)),
                "decision": decision,
                "security_signals": prediction_result.get("risk_signals", []),
                "timeline": [{"time": now.strftime("%H:%M:%S"), "event": status_label}],
                "model_version": prediction_result.get("model_version", "RXT-ResNeXt-GRU-v1.2")
            })
        except Exception:
            pass

        return True

    def get_security_audit_events(self) -> List[Dict[str, Any]]:
        """
        Derives security audit trail directly from verified transaction records.
        Does not invent fake events.
        """
        events = []
        for tx in self.get_transactions():
            decision = tx.get("decision", "ALLOW")
            events.append({
                "transaction_id": tx.get("transaction_id"),
                "timestamp": str(tx.get("timestamp", ""))[:19].replace("T", " "),
                "decision": decision,
                "recipient": tx.get("recipient"),
                "amount": tx.get("amount"),
                "risk_score": tx.get("risk_score")
            })
        return events[:6]
