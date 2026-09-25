"""
PayGuard AI - Authentication Service.
Handles database-backed user authentication, persistent registration,
and session lifecycle management.
"""

from typing import Optional, Dict, Any, Tuple
import re
import streamlit as st
from backend.app.database import db_manager
from frontend.data.mock_data import DEMO_USERS

class AuthService:
    """Manages database user authentication, registration, and session lifecycle."""

    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """Returns currently authenticated user session dictionary or None."""
        return st.session_state.get("authenticated_user", None)

    @staticmethod
    def login(identifier: str, pin: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticates against persistent SQLite database with fallback to demo accounts.
        Returns (success_boolean, error_message).
        """
        clean_id = (identifier or "").strip()
        clean_pin = (pin or "").strip()

        if not clean_id or not clean_pin:
            return False, "Please provide your Mobile Number / Email and Security PIN."

        # 1. Primary: Verify against SQLite Database
        try:
            auth_res = db_manager.authenticate_user(clean_id, clean_pin)
            if auth_res.get("success") and "user" in auth_res:
                user = auth_res["user"]
                st.session_state.authenticated_user = user
                
                # Initialize wallet balance from database
                if "wallet_balances" not in st.session_state:
                    st.session_state.wallet_balances = {}
                st.session_state.wallet_balances[user["user_id"]] = float(user.get("available_balance", 50000.0))
                
                st.session_state.current_screen = "home"
                st.session_state.login_error = None
                return True, None
            elif not auth_res.get("success"):
                db_err = auth_res.get("error")
            else:
                db_err = "Authentication failed."
        except Exception as ex:
            db_err = str(ex)

        # 2. Fallback: Check Demo Accounts (for demo fast access without network/db failure)
        demo_user = DEMO_USERS.get(clean_id)
        if demo_user and demo_user["pin"] == clean_pin:
            st.session_state.authenticated_user = demo_user
            if "wallet_balances" not in st.session_state:
                st.session_state.wallet_balances = {}
            if demo_user["user_id"] not in st.session_state.wallet_balances:
                st.session_state.wallet_balances[demo_user["user_id"]] = float(demo_user["initial_balance"])
            
            st.session_state.current_screen = "home"
            st.session_state.login_error = None
            return True, None

        return False, db_err or "Invalid credentials. Please verify your mobile number/email and security PIN."

    @staticmethod
    def register(
        name: str,
        mobile: str,
        email: str,
        pin: str,
        initial_balance: float = 50000.0
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Registers a new user into the database.
        Returns (success_boolean, error_message, user_dict).
        """
        clean_name = (name or "").strip()
        clean_mob = (mobile or "").strip().replace(" ", "").replace("-", "")
        clean_email = (email or "").strip().lower()
        clean_pin = (pin or "").strip()

        # Input Validations
        if not clean_name or len(clean_name) < 2:
            return False, "Please enter your valid full name.", None

        if len(clean_mob) == 12 and clean_mob.startswith("91"):
            clean_mob = clean_mob[2:]
        elif len(clean_mob) == 13 and clean_mob.startswith("+91"):
            clean_mob = clean_mob[3:]

        if not clean_mob.isdigit() or len(clean_mob) != 10:
            return False, "Please enter a valid 10-digit mobile number.", None

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, clean_email):
            return False, "Please enter a valid email address.", None

        if not clean_pin.isdigit() or len(clean_pin) != 4:
            return False, "Security PIN must be exactly 4 digits.", None

        if initial_balance < 0:
            return False, "Initial wallet balance cannot be negative.", None

        try:
            res = db_manager.register_user(
                name=clean_name,
                mobile=clean_mob,
                email=clean_email,
                pin=clean_pin,
                initial_balance=float(initial_balance)
            )

            if res.get("success") and "user" in res:
                return True, None, res["user"]
            else:
                return False, res.get("error", "Registration could not be completed."), None
        except Exception as ex:
            return False, f"Database error during registration: {str(ex)}", None

    @staticmethod
    def logout():
        """Clears all session-scoped state and resets back to login screen."""
        keys_to_clear = [
            "authenticated_user",
            "current_screen",
            "pending_payment",
            "security_result",
            "otp_error",
            "backend_health_status",
            "login_error",
            "reg_error",
            "reg_success"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_screen = "login"
        st.rerun()
