"""
PayGuard AI - Main Client-Facing Web Application Entry Point.
Router only: checks authentication, renders navigation, and routes between screens.
Run with: python -m streamlit run frontend/streamlit_app.py
"""

import os
import sys

# Ensure project root is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

# Configure Page Settings
st.set_page_config(
    page_title="PayGuard • Intelligent Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Inject Design Tokens and CSS from Single Source of Truth
from frontend.styles.theme import inject_theme
inject_theme()

# 2. Import Services and Components
from frontend.services.auth_service import AuthService
from frontend.components.navigation import render_navigation
from frontend.components.intro import render_intro
from frontend.components.login import render_login
from frontend.components.home import render_home
from frontend.components.payment import render_payment_flow
from frontend.components.transactions import render_transaction_history
from frontend.components.security import render_security_center
from frontend.components.profile import render_profile
from frontend.components.db_viewer import render_db_inspector

def main():
    # Authentication Check
    user = AuthService.get_current_user()

    if not user:
        # Check if user has entered the portal or wants to see the introduction overview
        if not st.session_state.get("intro_viewed", False):
            render_intro()
        else:
            render_login()
        return

    # Render Navigation & Get Active Screen
    active_screen = render_navigation()

    # Screen Routing
    if active_screen == "home":
        render_home()
    elif active_screen == "send_money":
        render_payment_flow()
    elif active_screen == "transactions":
        render_transaction_history()
    elif active_screen == "security_center":
        render_security_center()
    elif active_screen == "profile":
        render_profile()
    elif active_screen == "db_inspector":
        render_db_inspector()
    else:
        render_home()

if __name__ == "__main__":
    main()
