"""
PayGuard AI - Step-Up Real-Time Email OTP Verification Test Suite.
Verifies Risk Engine decision thresholds (26-65 -> VERIFY) and real-time email OTP dispatch/verification.
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.risk_engine import RiskEngine
from frontend.services.clerk_service import ClerkAuthService

def run_step_up_verification_tests():
    print("==================================================================")
    print("🔒 RUNNING STEP-UP REAL-TIME EMAIL OTP VERIFICATION TEST SUITE")
    print("==================================================================")

    risk_engine = RiskEngine()

    # 1. Test Risk Engine Decision Thresholds
    print("\n[1/4] Testing Risk Engine Decision Thresholds...")
    
    # ALLOW test (Score <= 25)
    res_allow = risk_engine.evaluate({"amount": 100.0}, 0.15)
    print(f"  • Score 15 -> Decision: {res_allow['decision']}")
    assert res_allow["decision"] == "ALLOW", f"Expected ALLOW, got {res_allow['decision']}"

    # VERIFY test (Score 26 to 65)
    res_verify_35 = risk_engine.evaluate({"amount": 15000.0, "is_new_device": True}, 0.35)
    print(f"  • Score 35 -> Decision: {res_verify_35['decision']}")
    assert res_verify_35["decision"] == "VERIFY", f"Expected VERIFY for score 35, got {res_verify_35['decision']}"

    res_verify_65 = risk_engine.evaluate({"amount": 25000.0, "is_new_location": True}, 0.65)
    print(f"  • Score 65 -> Decision: {res_verify_65['decision']}")
    assert res_verify_65["decision"] == "VERIFY", f"Expected VERIFY for score 65, got {res_verify_65['decision']}"

    # REVIEW test (Score > 65)
    res_review_85 = risk_engine.evaluate({"amount": 50000.0, "high_velocity": True, "is_new_device": True}, 0.85)
    print(f"  • Score 85 -> Decision: {res_review_85['decision']}")
    assert res_review_85["decision"] == "REVIEW", f"Expected REVIEW for score 85, got {res_review_85['decision']}"

    print("  ✅ Risk Engine Decision Thresholds (<=25 ALLOW, 26-65 VERIFY, >65 REVIEW) Verified!")

    # 2. Test Real-Time Clerk Email OTP Dispatch for Step-Up Verification
    test_user_email = "test_stepup_user@example.com"
    print(f"\n[2/4] Testing Real-Time Email OTP Dispatch for {test_user_email}...")
    success, status_msg, code_gen = ClerkAuthService.send_email_code(test_user_email)
    print(f"  • Dispatch status: {status_msg}")
    print(f"  • Generated OTP Code: '{code_gen}'")
    assert success is True
    assert len(code_gen) == 6

    # 3. Test Invalid Code Rejection
    print("\n[3/4] Testing Invalid Verification Code Rejection...")
    is_valid, msg = ClerkAuthService.verify_email_code(test_user_email, "999999")
    print(f"  • Invalid code result: is_valid={is_valid}, msg='{msg}'")
    assert is_valid is False

    # 4. Test Valid Code Verification
    print("\n[4/4] Testing Valid Email OTP Code Verification...")
    is_valid_real, msg_real = ClerkAuthService.verify_email_code(test_user_email, code_gen)
    print(f"  • Real OTP verification: is_valid={is_valid_real}, msg='{msg_real}'")
    assert is_valid_real is True

    # Test Clerk Dev Test Code '424242'
    is_valid_dev, msg_dev = ClerkAuthService.verify_email_code(test_user_email, "424242")
    print(f"  • Dev test code '424242' verification: is_valid={is_valid_dev}, msg='{msg_dev}'")
    assert is_valid_dev is True

    print("\n==================================================================")
    print("🎉 ALL STEP-UP EMAIL OTP VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    run_step_up_verification_tests()
