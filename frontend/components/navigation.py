"""
PayGuard AI - Navigation Component.
Renders clean fintech banking navigation sidebar and topbar indicator.
"""

import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.backend_api import BackendAPIService
from frontend.styles.theme import render_status_pill

def render_navigation() -> str:
    """
    Renders banking sidebar navigation with user card, nav items, and backend health status.
    Returns current active screen identifier.
    """
    user = AuthService.get_current_user()
    if not user:
        return "login"

    if "current_screen" not in st.session_state:
        st.session_state.current_screen = "home"

    api_service = BackendAPIService()
    health = api_service.check_health(force_refresh=False)

    with st.sidebar:
        # App Branding Header
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 12px 4px 20px 4px; border-bottom: 1px solid #EDEFF3; margin-bottom: 20px;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: #2F5FDE; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 20px; font-weight: 800; box-shadow: 0 4px 10px rgba(47, 95, 222, 0.25);">
                🛡️
            </div>
            <div>
                <div style="font-weight: 800; font-size: 17px; color: #0B1D33; letter-spacing: -0.02em; line-height: 1.2;">
                    PayGuard
                </div>
                <div style="font-size: 11px; color: #6B7280; font-weight: 500;">
                    Intelligent Protection
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Active User Summary Card
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #EDEFF3; border-radius: 12px; padding: 12px 14px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(15,23,42,0.03);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 36px; height: 36px; border-radius: 50%; background: #EEF3FF; color: #2F5FDE; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px;">
                    {user.get("avatar_initials", "U")}
                </div>
                <div style="overflow: hidden;">
                    <div style="font-weight: 600; font-size: 13px; color: #0B1D33; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                        {user.get("name", "User")}
                    </div>
                    <div style="font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">
                        +91 {user.get("mobile", "")}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Options
        nav_options = [
            ("home", "🏠 Home / Wallet"),
            ("send_money", "💸 Send Money"),
            ("transactions", "📋 Transaction History"),
            ("security_center", "🛡 Security Center"),
            ("profile", "👤 Profile")
        ]

        st.markdown('<div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Navigation</div>', unsafe_allow_html=True)

        for screen_key, label in nav_options:
            is_active = st.session_state.current_screen == screen_key
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"nav_btn_{screen_key}", use_container_width=True, type=btn_type):
                # If currently on send_money flow, reset pending states when switching tabs
                if screen_key != "send_money":
                    st.session_state.pop("pending_payment", None)
                    st.session_state.pop("security_result", None)
                st.session_state.current_screen = screen_key
                st.rerun()

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

        # Backend Engine Telemetry Status Widget
        status_text = health.get("status_label", "Offline")
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #EDEFF3; border-radius: 12px; padding: 12px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">FastAPI Engine</span>
                {render_status_pill(status_text)}
            </div>
            <div style="font-size: 10px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">
                Model: {health.get('model_version', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_ref, col_out = st.columns([1, 1])
        with col_ref:
            if st.button("🔄 Check", help="Query FastAPI /api/v1/health status", use_container_width=True):
                api_service.check_health(force_refresh=True)
                st.rerun()
        with col_out:
            if st.button("🚪 Logout", use_container_width=True):
                AuthService.logout()

        # Unobtrusive Sandbox Notice Footer
        st.markdown("""
        <div style="margin-top: 30px; text-align: center;">
            <div style="display: inline-block; font-size: 10px; font-weight: 700; color: #6B7280; background: #EDEFF3; padding: 4px 10px; border-radius: 999px; letter-spacing: 0.05em;">
                SANDBOX • NO REAL MONEY
            </div>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.current_screen
