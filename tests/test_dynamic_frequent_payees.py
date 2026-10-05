"""
Test Script: Dynamic Frequent Payees Verification
1. Register a new user and verify that Frequent Payees starts EMPTY ([]).
2. Complete a payment to a payee.
3. Verify that the payee is automatically added to SQLite DB beneficiaries table and returned in get_frequent_payees().
"""

import sys
import os
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class SessionStateMock(dict):
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value

if not hasattr(st, 'session_state') or not isinstance(st.session_state, SessionStateMock):
    st.session_state = SessionStateMock()
if "wallet_balances" not in st.session_state:
    st.session_state.wallet_balances = {}
if "session_transactions" not in st.session_state:
    st.session_state.session_transactions = []

from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService
from backend.app.database import db_manager

def main():
    print("==================================================================")
    print("🧪 TESTING DYNAMIC FREQUENT PAYEES FOR NEW & EXISTING USERS")
    print("==================================================================")

    # Step 1: Register New User
    print("\n[1/4] Registering new user (Deepak Kumar)...")
    reg_ok, reg_err, new_u = AuthService.register(
        name="Deepak Kumar",
        mobile="9899887766",
        email="deepak.kumar@test.com",
        pin="1234",
        password="DeepakPassword123!"
    )
    assert reg_ok is True, f"Registration failed: {reg_err}"
    user_id = new_u["user_id"]
    print(f"  ✅ Registration successful! User ID: {user_id}")

    # Step 2: Verify Frequent Payees is EMPTY for New User
    print("\n[2/4] Verifying Frequent Payees list is EMPTY for new user...")
    tx_service = MockTransactionService(user_id)
    payees_initial = tx_service.get_frequent_payees()
    print(f"  Initial Payees Count: {len(payees_initial)}")
    assert len(payees_initial) == 0, f"Expected 0 frequent payees for new user, got: {payees_initial}"
    print("  ✅ Confirmed: New user has 0 frequent payees!")

    # Step 3: Complete a Payment
    print("\n[3/4] Completing a money transfer to Rohan Verma (rohan.v@upi)...")
    import random
    tx_id = random.randint(100000, 999999)
    success = tx_service.record_completed_transaction(
        transaction_id=tx_id,
        recipient="Rohan Verma",
        recipient_id="rohan.v@upi",
        amount=2500.0,
        prediction_result={
            "decision": "ALLOW",
            "risk_score": 10,
            "fraud_probability": 0.05,
            "risk_signals": ["Normal transaction"]
        }
    )
    assert success is True, "Payment completion failed!"
    print("  ✅ Payment recorded successfully!")

    # Step 4: Verify Payee Automatically Added to DB & Frequent Payees List
    print("\n[4/4] Verifying Frequent Payees updated in SQLite DB...")
    payees_after = tx_service.get_frequent_payees()
    print(f"  Payees Count After Payment: {len(payees_after)}")
    assert len(payees_after) == 1, f"Expected 1 frequent payee after payment, got: {len(payees_after)}"
    assert payees_after[0]["name"] == "Rohan Verma", f"Payee name mismatch: {payees_after[0]}"
    assert payees_after[0]["identifier"] == "rohan.v@upi", f"Payee ID mismatch: {payees_after[0]}"
    print(f"  ✅ Payee automatically added: {payees_after[0]}")

    # Inspect SQLite DB beneficiaries table
    conn = db_manager._get_sqlite_conn()
    row = conn.execute("SELECT * FROM beneficiaries WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    assert row is not None, "Beneficiary row not found in SQLite DB!"
    print(f"  ✅ Persisted SQLite DB Beneficiary Row: Name='{row['name']}', UPI='{row['upi_id']}', Frequent={row['is_frequent']}")

    # Clean up test user
    conn = db_manager._get_sqlite_conn()
    conn.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM beneficiaries WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    print("\n==================================================================")
    print("🎉 DYNAMIC FREQUENT PAYEES TEST PASSED 100% SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    main()
