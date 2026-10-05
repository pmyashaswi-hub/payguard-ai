"""
Verification Script for PayGuard AI:
1. Register user with Name, Mobile, Email, Password, and UPI PIN.
2. Inspect SQLite DB to verify user record is saved.
3. Test login with wrong password (should fail).
4. Test login with correct password (should succeed and authenticate).
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

from frontend.services.auth_service import AuthService
from backend.app.database import db_manager

def main():
    print("==================================================================")
    print("🧪 VERIFYING DATABASE REGISTRATION & LOGIN AUTHENTICATION")
    print("==================================================================")

    test_name = "Yashaswi P M"
    test_mobile = "9876501234"
    test_email = "pmyashaswi@gmail.com"
    test_pass = "YashaswiPass2026!"
    test_pin = "1234"

    # Step 1: Register User
    print(f"\n[1/4] Registering user: {test_name} ({test_email})...")
    reg_ok, reg_err, new_u = AuthService.register(
        name=test_name,
        mobile=test_mobile,
        email=test_email,
        pin=test_pin,
        password=test_pass
    )
    assert reg_ok is True, f"Registration failed: {reg_err}"
    print(f"  ✅ Registration successful! User ID: {new_u['user_id']}")

    # Step 2: Query SQLite Database
    print("\n[2/4] Querying SQLite payguard_bank.db for saved record...")
    conn = db_manager._get_sqlite_conn()
    row = conn.execute("SELECT user_id, name, email, mobile, password_hash, pin_hash FROM users WHERE email = ?", (test_email,)).fetchone()
    conn.close()

    assert row is not None, "User record not found in SQLite DB!"
    print(f"  ✅ User found in DB!")
    print(f"     Name: {row['name']}")
    print(f"     Mobile: {row['mobile']}")
    print(f"     Email: {row['email']}")
    print(f"     Password Hash (SHA-256): {row['password_hash'][:30]}...")
    print(f"     PIN Hash (SHA-256): {row['pin_hash'][:30]}...")

    # Step 3: Test Login with WRONG Password
    print("\n[3/4] Testing login with WRONG password...")
    wrong_ok, wrong_err = AuthService.login(test_email, "WrongPassword999!")
    assert wrong_ok is False, "Login with wrong password succeeded improperly!"
    print(f"  ✅ Wrong password correctly rejected: '{wrong_err}'")

    # Step 4: Test Login with CORRECT Password
    print("\n[4/4] Testing login with CORRECT password...")
    right_ok, right_err = AuthService.login(test_email, test_pass)
    assert right_ok is True, f"Login with correct password failed: {right_err}"
    authenticated_user = st.session_state.authenticated_user
    print(f"  ✅ Login successful! Authenticated User in Session: {authenticated_user['name']} ({authenticated_user['email']})")

    # Clean up test row
    conn = db_manager._get_sqlite_conn()
    conn.execute("DELETE FROM beneficiaries WHERE user_id = ?", (new_u['user_id'],))
    conn.execute("DELETE FROM users WHERE user_id = ?", (new_u['user_id'],))
    conn.commit()
    conn.close()

    print("\n==================================================================")
    print("🎉 ALL REGISTRATION AND LOGIN AUTHENTICATION VERIFICATIONS PASSED!")
    print("==================================================================")

if __name__ == "__main__":
    main()
