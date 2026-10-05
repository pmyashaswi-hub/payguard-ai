"""
Test Script: Clerk Email Verification & Auth Flow Test for PayGuard AI.
Verifies Clerk code generation, standard dev test code '424242' validation,
Clerk API configuration checks, and database user creation.
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

from frontend.services.clerk_service import ClerkAuthService
from frontend.services.auth_service import AuthService

def run_tests():
    print("==================================================================")
    print("🔒 RUNNING CLERK AUTH & EMAIL VERIFICATION TEST SUITE (clerk.com)")
    print("==================================================================")

    test_email = f"clerk_user_{random.randint(1000, 9999)}@example.com"
    test_pin = "4321"

    # Step 1: Check Clerk Configuration
    print("\n[1/5] Checking Clerk API key configuration...")
    is_conf = ClerkAuthService.is_clerk_configured()
    pub_key, sec_key, api_url = ClerkAuthService.get_clerk_keys()
    print(f"  ℹ️ Clerk Configured: {is_conf}")
    print(f"  ℹ️ Clerk API Endpoint: {api_url}")

    # Step 2: Send Code via Clerk Auth Service
    print(f"\n[2/5] Dispatching Clerk verification code to {test_email}...")
    success, msg, code = ClerkAuthService.send_email_code(test_email)
    assert success is True, f"Failed to send Clerk code: {msg}"
    assert len(code) == 6 and code.isdigit(), f"Invalid code format: {code}"
    print(f"  ✅ Code generated: '{code}'")
    print(f"  ✅ Status message: {msg}")

    # Step 3: Verify Invalid Code
    print("\n[3/5] Testing invalid Clerk verification code...")
    wrong_code = "000000" if code != "000000" else "999999"
    ok_wrong, msg_wrong = ClerkAuthService.verify_email_code(test_email, wrong_code)
    assert ok_wrong is False, "Invalid code was accepted!"
    print("  ✅ Invalid code correctly rejected!")

    # Step 4: Verify Clerk Standard Dev Code '424242' and Generated Code
    print("\n[4/5] Testing Clerk dev test code '424242' and generated code...")
    ok_dev, msg_dev = ClerkAuthService.verify_email_code(test_email, "424242")
    assert ok_dev is True, f"Clerk dev code 424242 failed: {msg_dev}"
    print(f"  ✅ Clerk dev test code '424242' verified: {msg_dev}")

    ok_gen, msg_gen = ClerkAuthService.verify_email_code(test_email, code)
    assert ok_gen is True, f"Generated code failed: {msg_gen}"
    print(f"  ✅ Generated code '{code}' verified: {msg_gen}")

    # Step 5: User Registration after Clerk Verification
    print(f"\n[5/5] Registering user in SQLite database after Clerk verification...")
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
    assert new_user is not None, "User object null!"
    print(f"  ✅ User registered in DB after Clerk verification! User ID: {new_user['user_id']}")

    print("\n==================================================================")
    print("🎉 ALL CLERK AUTHENTICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
