"""
Test Script: Email + Password Authentication & UPI PIN Verification Test for PayGuard AI.
Verifies separate hashing of Password vs 4-Digit UPI PIN, registration, and login.
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

# Mock Streamlit session state
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
    print("🧪 TESTING EMAIL + PASSWORD AUTHENTICATION & DATABASE SYNC")
    print("==================================================================")

    test_email = f"user_{random.randint(1000, 9999)}@gmail.com"
    test_password = "MySecretPassword123!"
    test_pin = "9876"

    # Step 1: Register User in Database
    print(f"\n[1/4] Registering new user ({test_email})...")
    derived_name = "Test User"
    derived_mob = f"98{random.randint(10000000, 99999999)}"

    reg_success, reg_err, new_user = AuthService.register(
        name=derived_name,
        mobile=derived_mob,
        email=test_email,
        pin=test_pin,
        password=test_password,
        initial_balance=50000.0
    )

    assert reg_success is True, f"Registration failed: {reg_err}"
    assert new_user is not None, "User object null!"
    assert new_user["email"] == test_email, "Email mismatch!"
    print(f"  ✅ Registration successful! User ID: {new_user['user_id']}")

    # Step 2: Test Login with WRONG Password
    print("\n[2/4] Testing login with WRONG password...")
    wrong_login_ok, wrong_login_err = AuthService.login(test_email, "WrongPassword999!")
    assert wrong_login_ok is False, "Login with wrong password succeeded improperly!"
    print(f"  ✅ Wrong password correctly rejected: '{wrong_login_err}'")

    # Step 3: Test Login with CORRECT Password
    print("\n[3/4] Testing login with CORRECT password...")
    correct_login_ok, correct_login_err = AuthService.login(test_email, test_password)
    assert correct_login_ok is True, f"Login with correct password failed: {correct_login_err}"
    print(f"  ✅ Correct password verified! Session User: {st.session_state.authenticated_user['name']}")

    # Step 4: Test 4-Digit UPI PIN Verification
    print("\n[4/4] Testing 4-digit UPI PIN verification for transfers...")
    user_id = new_user["user_id"]
    pin_ok = db_manager.verify_upi_pin(user_id, test_pin)
    assert pin_ok is True, "UPI PIN verification failed!"
    print("  ✅ 4-Digit UPI PIN verified successfully in database!")

    print("\n==================================================================")
    print("🎉 ALL EMAIL + PASSWORD AUTHENTICATION TESTS PASSED!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
