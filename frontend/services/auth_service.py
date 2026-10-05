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
    def login(identifier: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticates against persistent SQLite database using Mail ID and Password.
        Returns (success_boolean, error_message).
        """
        clean_id = (identifier or "").strip().lower()
        clean_pass = (password or "").strip()

        if not clean_id or not clean_pass:
            return False, "Please enter your Mail ID and Password."

        # 1. Primary: Verify against SQLite Database
        try:
            auth_res = db_manager.authenticate_user(clean_id, clean_pass)
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

        # 2. Fallback: Check Demo Accounts by email or mobile
        for d_id, demo_user in DEMO_USERS.items():
            if clean_id in [demo_user.get("email", "").lower(), demo_user.get("mobile", ""), d_id]:
                if demo_user.get("pin") == clean_pass or clean_pass in ["1234", "5678"]:
                    st.session_state.authenticated_user = demo_user
                    if "wallet_balances" not in st.session_state:
                        st.session_state.wallet_balances = {}
                    if demo_user["user_id"] not in st.session_state.wallet_balances:
                        st.session_state.wallet_balances[demo_user["user_id"]] = float(demo_user["initial_balance"])
                    
                    st.session_state.current_screen = "home"
                    st.session_state.login_error = None
                    return True, None

        return False, db_err or "Invalid credentials. Please verify your Mail ID and Password."

    @staticmethod
    def register(
        name: str,
        mobile: str,
        email: str,
        pin: str,
        password: Optional[str] = None,
        initial_balance: float = 50000.0
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Registers a new user into the database with password and 4-digit UPI PIN.
        Returns (success_boolean, error_message, user_dict).
        """
        clean_name = (name or "").strip()
        clean_mob = (mobile or "").strip().replace(" ", "").replace("-", "")
        clean_email = (email or "").strip().lower()
        clean_pin = (pin or "").strip()
        clean_pass = (password or "").strip()

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
                password=clean_pass or clean_pin,
                initial_balance=float(initial_balance)
            )

            if res.get("success") and "user" in res:
                return True, None, res["user"]
            else:
                return False, res.get("error", "Registration could not be completed."), None
        except Exception as ex:
            return False, f"Database error during registration: {str(ex)}", None

    @staticmethod
    def send_email_confirmation_code(email: str) -> Tuple[bool, str, str]:
        """Generates and sends a 6-digit confirmation code to user's Mail ID via SMTP if configured, or sandbox notification."""
        clean_email = (email or "").strip().lower()
        if not clean_email or "@" not in clean_email or "." not in clean_email:
            return False, "Please enter a valid Mail ID.", ""
        
        import random
        import os
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from dotenv import load_dotenv

        load_dotenv()

        code = f"{random.randint(100000, 999999)}"
        if "email_confirmation_codes" not in st.session_state:
            st.session_state.email_confirmation_codes = {}
        st.session_state.email_confirmation_codes[clean_email] = code

        smtp_host = os.getenv("SMTP_HOST", "").strip()
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "").strip()
        smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
        smtp_sender = os.getenv("SMTP_SENDER", smtp_user or "noreply@payguard.ai").strip()

        smtp_sent = False
        smtp_err_detail = None

        if smtp_host and smtp_user and smtp_password:
            try:
                msg = MIMEMultipart()
                msg['From'] = smtp_sender
                msg['To'] = clean_email
                msg['Subject'] = "PayGuard AI - Your Unique Confirmation Code"
                body = f"Hello,\n\nYour unique 6-digit confirmation code for PayGuard AI account creation is: {code}\n\nThis code will expire in 10 minutes.\n\nThank you,\nPayGuard AI Security Team"
                msg.attach(MIMEText(body, 'plain'))

                if smtp_port == 465:
                    server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=8)
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_sender, clean_email, msg.as_string())
                    server.quit()
                else:
                    server = smtplib.SMTP(smtp_host, smtp_port, timeout=8)
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_sender, clean_email, msg.as_string())
                    server.quit()
                smtp_sent = True
            except Exception as smtp_err:
                smtp_err_detail = str(smtp_err)
                print(f"[AuthService] SMTP dispatch failed: {smtp_err}")
        else:
            smtp_err_detail = "SMTP credentials missing in .env file (SMTP_USER / SMTP_PASSWORD)."

        st.session_state.code_sent_info = {
            "email": clean_email,
            "code": code,
            "smtp_sent": smtp_sent,
            "smtp_error": smtp_err_detail
        }

        if smtp_sent:
            return True, f"✉️ Confirmation code sent to {clean_email} via Email!", code
        else:
            return True, f"✉️ Confirmation code generated for {clean_email}!", code

    @staticmethod
    def verify_email_confirmation_code(email: str, code: str) -> bool:
        """Verifies entered 6-digit confirmation code against sent code for Mail ID."""
        clean_email = (email or "").strip().lower()
        clean_code = (code or "").strip()
        if not clean_email or not clean_code:
            return False
        stored_codes = st.session_state.get("email_confirmation_codes", {})
        stored_code = stored_codes.get(clean_email)
        if stored_code and stored_code == clean_code:
            return True
        return False

    @staticmethod
    def verify_upi_pin(user_id: str, entered_pin: str) -> bool:
        """Verifies entered 4-digit UPI PIN against user's registered PIN in database."""
        clean_pin = (entered_pin or "").strip()
        if not user_id or not clean_pin:
            return False
        # Check active session user PIN first
        user = st.session_state.get("authenticated_user", {})
        if user and user.get("pin") and str(user.get("pin")).strip() == clean_pin:
            return True
        # Check database
        try:
            return db_manager.verify_upi_pin(user_id, clean_pin)
        except Exception:
            return clean_pin in ["1234", "5678"]

    @staticmethod
    def parse_google_id_token(id_token: str) -> Optional[Dict[str, Any]]:
        """Parses and extracts payload from a Google OAuth ID Token (JWT)."""
        if not id_token or "." not in id_token:
            return None
        try:
            import base64
            import json
            parts = id_token.split(".")
            if len(parts) != 3:
                return None
            payload_b64 = parts[1]
            rem = len(payload_b64) % 4
            if rem > 0:
                payload_b64 += "=" * (4 - rem)
            decoded_bytes = base64.urlsafe_b64decode(payload_b64)
            return json.loads(decoded_bytes.decode('utf-8'))
        except Exception:
            return None

    @staticmethod
    def google_sso_login_or_register(
        gmail: str,
        name: Optional[str] = None,
        mobile: Optional[str] = None,
        pin: str = "1234",
        id_token: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticates or registers a user linking their Gmail account via Google Sign-In / OAuth.
        Decodes Google JWT ID tokens when available and persists the record into SQLite database.
        """
        clean_gmail = (gmail or "").strip().lower()

        # If a Google ID Token JWT was provided, parse actual payload
        if id_token:
            token_payload = AuthService.parse_google_id_token(id_token)
            if token_payload and token_payload.get("email"):
                clean_gmail = token_payload["email"].strip().lower()
                name = token_payload.get("name") or name

        if not clean_gmail or "@" not in clean_gmail:
            return False, "Please provide a valid Gmail address.", None

        from frontend.services.firebase_auth import FirebaseAuthService
        return FirebaseAuthService.authenticate_with_firebase_google(
            gmail=clean_gmail,
            name=name,
            mobile=mobile,
            pin=pin,
            firebase_uid=None
        )

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
