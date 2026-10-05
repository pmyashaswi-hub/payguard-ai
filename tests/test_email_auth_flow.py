"""
Test Script: Email Confirmation Code & Account Creation Verification for PayGuard AI.
Verifies unique 6-digit code generation, SMTP/Sandbox handling, code verification,
and persistent database registration with 4-digit UPI PIN.
"""

import sys
import os
import random

# Ensure root dir is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Mock Streamlit session state for testing outside Streamlit runner
class SessionStateMock(dict):
    def __getattr__(self, name):
        return self.get(name)
    def __setattr__(self, name, value):
        self[name] = value

import streamlit as st
if not hasattr(st, 'session_state') or not isinstance(st.session_state, SessionStateMock):
    st.session_state = SessionStateMock()

from frontend.services.auth_service import AuthService
from backend.app.database import db_manager

def run_tests():
    print("==================================================================")
    print("🧪 RUNNING PAYGUARD AI EMAIL CONFIRMATION & AUTH TEST SUITE")
    print("==================================================================")

    test_email = f"testuser_{random.randint(1000, 9999)}@example.com"
    test_password = "SecurePass123!"
    test_pin = "4321"

    # Step 1: Request Confirmation Code
    print(f"\n[1/4] Requesting 6-digit confirmation code for {test_email}...")
    success, msg, code = AuthService.send_email_confirmation_code(test_email)
    assert success is True, f"Failed to send confirmation code: {msg}"
    assert len(code) == 6 and code.isdigit(), f"Invalid code format: {code}"
    print(f"  ✅ Code successfully generated: '{code}'")
    print(f"  ✅ Dispatch message: {msg}")

    # Step 2: Verify Incorrect Code Rejection
    print("\n[2/4] Testing code verification with invalid code...")
    wrong_code = "000000" if code != "000000" else "999999"
    is_valid_wrong = AuthService.verify_email_confirmation_code(test_email, wrong_code)
    assert is_valid_wrong is False, "Incorrect code was improperly accepted!"
    print("  ✅ Invalid code correctly rejected!")

    # Step 3: Verify Correct Code
    print("\n[3/4] Testing code verification with correct code...")
    is_valid_correct = AuthService.verify_email_confirmation_code(test_email, code)
    assert is_valid_correct is True, "Valid code was rejected!"
    print("  ✅ Correct code verified successfully!")

    # Step 4: Register New User in Database
    print(f"\n[4/4] Registering user in SQLite database ({test_email})...")
    derived_name = test_email.split("@")[0].title()
    derived_mob = f"98{random.randint(10000000, 99999999)}"

    reg_success, reg_err, new_user = AuthService.register(
        name=derived_name,
        mobile=derived_mob,
        email=test_email,
        pin=test_pin,
        initial_balance=50000.0
    )

    assert reg_success is True, f"Registration failed: {reg_err}"
    assert new_user is not None, "User object was not returned!"
    assert new_user["email"] == test_email, "Email mismatch in registered user!"
    print(f"  ✅ User successfully registered in DB! User ID: {new_user['user_id']}")

    # Step 5: Test Login with new user
    print("\n[5/5] Testing login with newly created user credentials...")
    login_success, login_err = AuthService.login(test_email, test_pin)
    assert login_success is True, f"Login failed for new user: {login_err}"
    print(f"  ✅ Login successful! Active session user: {st.session_state.authenticated_user['name']}")

    print("\n==================================================================")
    print("🎉 ALL EMAIL AUTHENTICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
