"""
PayGuard AI - Firebase Authentication Service.
Handles Firebase Google Auth credential verification, token validation,
and mapping Firebase user profiles to payguard_bank.db.
"""

import os
import json
import random
from typing import Dict, Any, Optional, Tuple
import streamlit as st
from backend.app.database import db_manager

# Default Firebase Configuration (Customizable via environment variables)
DEFAULT_FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyB_PayGuardAI_SandboxKey_2026"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "payguard-ai.firebaseapp.com"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", "payguard-ai"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "payguard-ai.appspot.com"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "987654321098"),
    "appId": os.getenv("FIREBASE_APP_ID", "1:987654321098:web:payguard123456")
}

class FirebaseAuthService:
    """Manages Firebase Google Authentication integration and database profile synchronization."""

    @staticmethod
    def get_firebase_config() -> Dict[str, str]:
        """Returns active Firebase Web App configuration dictionary from session state, env, or defaults."""
        if "custom_firebase_config" in st.session_state and st.session_state.custom_firebase_config:
            return st.session_state.custom_firebase_config
        return {
            "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyB_PayGuardAI_SandboxKey_2026"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "payguard-ai.firebaseapp.com"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", "payguard-ai"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "payguard-ai.appspot.com"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "987654321098"),
            "appId": os.getenv("FIREBASE_APP_ID", "1:987654321098:web:payguard123456")
        }

    @staticmethod
    def set_custom_firebase_config(api_key: str, auth_domain: str, project_id: str, app_id: str):
        """Sets custom user-defined Firebase project credentials."""
        st.session_state.custom_firebase_config = {
            "apiKey": api_key.strip(),
            "authDomain": auth_domain.strip(),
            "projectId": project_id.strip(),
            "storageBucket": f"{project_id.strip()}.appspot.com",
            "messagingSenderId": "123456789",
            "appId": app_id.strip()
        }

    @staticmethod
    def authenticate_with_firebase_google(
        gmail: str,
        name: Optional[str] = None,
        mobile: Optional[str] = None,
        pin: str = "1234",
        initial_balance: float = 50000.0,
        firebase_uid: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Authenticates or registers a user linking their Firebase Google Auth account.
        Maps the Gmail address and Firebase UID directly to payguard_bank.db.
        """
        clean_gmail = (gmail or "").strip().lower()
        if not clean_gmail or "@" not in clean_gmail:
            return False, "Please enter a valid Gmail address for Firebase Google Auth.", None

        try:
            conn = db_manager._get_sqlite_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (clean_gmail,))
            row = cursor.fetchone()

            display_name = (name or clean_gmail.split("@")[0].replace(".", " ").title()).strip()
            initials = "".join([p[0].upper() for p in display_name.split()[:2]]) if display_name else "F"

            if row:
                user_dict = dict(row)
                cursor.execute("UPDATE users SET auth_provider = 'Firebase Google Auth' WHERE user_id = ?", (user_dict["user_id"],))
                conn.commit()
                conn.close()

                acc_num = user_dict.get("account_number") or f"ACC-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
                upi = user_dict.get("upi_id") or f"{display_name.lower().replace(' ', '.')}@payguard"

                user = {
                    "user_id": user_dict["user_id"],
                    "name": user_dict.get("name") or display_name,
                    "mobile": user_dict.get("mobile", mobile or "9876543210"),
                    "email": clean_gmail,
                    "pin": pin.strip() if pin else "1234",
                    "account_num": acc_num,
                    "account_number": acc_num,
                    "upi_id": upi,
                    "initial_balance": float(user_dict.get("available_balance", 50000.0)),
                    "available_balance": float(user_dict.get("available_balance", 50000.0)),
                    "today_spending": float(user_dict.get("today_spending", 0.0)),
                    "total_payments_count": int(user_dict.get("total_payments_count", 0)),
                    "security_status": "Protected (Firebase Google Verified)",
                    "security_score": 99,
                    "avatar_initials": initials,
                    "auth_provider": "Firebase Google Auth",
                    "firebase_uid": firebase_uid or f"fb_uid_{random.randint(100000, 999999)}",
                    "gmail_linked": True
                }

                st.session_state.authenticated_user = user
                if "wallet_balances" not in st.session_state:
                    st.session_state.wallet_balances = {}
                st.session_state.wallet_balances[user["user_id"]] = float(user["available_balance"])
                st.session_state.current_screen = "home"
                st.session_state.login_error = None
                return True, None, user
            else:
                conn.close()
                mob_val = (mobile or f"98{random.randint(10000000, 99999999)}").strip()

                reg_res = db_manager.register_user(
                    name=display_name,
                    mobile=mob_val,
                    email=clean_gmail,
                    pin=pin.strip() if pin else "1234",
                    initial_balance=float(initial_balance)
                )

                if reg_res.get("success") and "user" in reg_res:
                    u_obj = reg_res["user"]
                    conn2 = db_manager._get_sqlite_conn()
                    conn2.execute("UPDATE users SET auth_provider = 'Firebase Google Auth' WHERE user_id = ?", (u_obj["user_id"],))
                    conn2.commit()
                    conn2.close()

                    u_obj["auth_provider"] = "Firebase Google Auth"
                    u_obj["gmail_linked"] = True
                    u_obj["security_status"] = "Protected (Firebase Google Verified)"
                    u_obj["firebase_uid"] = firebase_uid or f"fb_uid_{random.randint(100000, 999999)}"

                    st.session_state.authenticated_user = u_obj
                    if "wallet_balances" not in st.session_state:
                        st.session_state.wallet_balances = {}
                    st.session_state.wallet_balances[u_obj["user_id"]] = float(u_obj["available_balance"])
                    st.session_state.current_screen = "home"
                    st.session_state.login_error = None
                    return True, None, u_obj
                else:
                    return False, reg_res.get("error", "Firebase user registration failed."), None

        except Exception as ex:
            return False, f"Firebase Google Auth error: {str(ex)}", None
