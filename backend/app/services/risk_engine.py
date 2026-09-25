"""
Risk Engine Service: Evaluates RXT fraud probability, anomaly signals, and transaction ledger integrity.
"""

from typing import Dict, Any, List

class RiskEngine:
    def evaluate(self, data: Dict[str, Any], fraud_prob: float) -> Dict[str, Any]:
        """
        Computes composite risk score, decision tier, security signals, and ledger state consistency.
        """
        risk_score = int(round(fraud_prob * 100))
        
        # Decision Tiers
        if risk_score < 25:
            decision = "ALLOW"
        elif risk_score < 65:
            decision = "VERIFY"
        else:
            decision = "REVIEW"

        # Signal Generation
        signals: List[str] = []
        amount = float(data.get("amount", 0.0))
        is_new_device = bool(data.get("is_new_device", False))
        is_new_location = bool(data.get("is_new_location", False))
        high_velocity = bool(data.get("high_velocity", False))
        failed_attempts = int(data.get("failed_attempts", 0))

        if amount > 40000.0:
            signals.append("High transaction amount surge (> 5x normal profile)")
        elif amount > 10000.0:
            signals.append("Elevated single transaction amount")

        if is_new_device:
            signals.append("New device detected (Unrecognized fingerprint)")
        
        if is_new_location:
            signals.append("Unusual location / VPN access detected")

        if high_velocity:
            signals.append("High transaction velocity in active window")

        if failed_attempts > 0:
            signals.append(f"{failed_attempts} failed security attempts recorded")

        if not signals:
            signals.append("Normal transaction amount for profile")
            signals.append("Recognized device fingerprint")
            signals.append("Low velocity in sliding window")

        # Transaction Ledger Integrity Check
        sender_debited = bool(data.get("sender_debited", True))
        receiver_credited = bool(data.get("receiver_credited", True))
        gateway_status = str(data.get("gateway_status", "SUCCESS"))
        settlement_status = str(data.get("settlement_status", "COMPLETED"))

        is_consistent = True
        inconsistency_reason = None

        if sender_debited and not receiver_credited and gateway_status == "SUCCESS":
            is_consistent = False
            inconsistency_reason = "Sender debited but recipient account not credited"
        elif not sender_debited and receiver_credited:
            is_consistent = False
            inconsistency_reason = "Receiver credited without sender debit"

        integrity_data = {
            "sender_debited": sender_debited,
            "receiver_credited": receiver_credited,
            "gateway_status": gateway_status,
            "settlement_status": settlement_status,
            "is_consistent": is_consistent,
            "inconsistency_reason": inconsistency_reason
        }

        return {
            "fraud_probability": round(fraud_prob, 4),
            "risk_score": risk_score,
            "decision": decision,
            "risk_signals": signals,
            "transaction_integrity": integrity_data
        }
