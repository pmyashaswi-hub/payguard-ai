"""
PayGuard AI - Introduction & Project Overview Webpage.
Exact pixel-perfect implementation matching the official PayGuard hero mockup design.
Fitted for 100% desktop site viewports with zero vertical scroll required.
"""

import os
import streamlit as st
from frontend.services.backend_api import BackendAPIService
from frontend.styles.theme import render_status_pill

def render_intro():
    """Renders the pixel-perfect PayGuard hero overview page fitted for 100% desktop site viewports."""
    api_service = BackendAPIService()
    health = api_service.check_health(force_refresh=False)
    backend_status = health.get("status_label", "Connected")

    # Custom Dot Grid Background & Button Styles Injection
    st.markdown("""<style>
.stApp {
    background-color: #F8FAFC !important;
    background-image: radial-gradient(#CBD5E1 1.2px, transparent 1.2px) !important;
    background-size: 24px 24px !important;
}

button[key="top_btn_signin"] {
    border-radius: 999px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #0F172A !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
}
button[key="top_btn_register"] {
    border-radius: 999px !important;
    background-color: #0A2540 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 10px rgba(10, 37, 64, 0.2) !important;
}

button[key="hero_btn_signin_acc"] {
    border-radius: 999px !important;
    background-color: #0A2540 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(10, 37, 64, 0.25) !important;
}
button[key="hero_btn_register_acc"] {
    border-radius: 999px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #7BBDE8 !important;
    color: #0A2540 !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
}
</style>""", unsafe_allow_html=True)

    # 1. TOP COMPACT NAVIGATION HEADER
    col_nav_brand, col_nav_action = st.columns([1.3, 1.1])
    with col_nav_brand:
        st.markdown("""<div style="display: flex; align-items: center; gap: 12px; padding: 2px 0 10px 0;">
<div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 20px; font-weight: 800; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);">🛡️</div>
<div>
<div style="font-weight: 800; font-size: 20px; color: #0F172A; letter-spacing: -0.02em; line-height: 1.1;">PayGuard</div>
<div style="font-size: 11px; color: #64748B; font-weight: 500;">Intelligent Payment Protection</div>
</div>
</div>""", unsafe_allow_html=True)

    with col_nav_action:
        c_stat, c_l, c_r = st.columns([1.1, 0.9, 1.0])
        with c_stat:
            st.markdown(f"""<div style="text-align: right; padding-top: 8px; font-size: 11.5px; color: #64748B; font-weight: 600;">Backend: <span style="display: inline-block; background: #DCFCE7; color: #166534; border-radius: 999px; padding: 2px 10px; font-size: 11px; font-weight: 700;">&bull; {backend_status}</span></div>""", unsafe_allow_html=True)
        with c_l:
            if st.button("Sign In", key="top_btn_signin", use_container_width=True):
                st.session_state.intro_viewed = True
                st.session_state.auth_mode = "login"
                st.rerun()
        with c_r:
            if st.button("Register", type="primary", key="top_btn_register", use_container_width=True):
                st.session_state.intro_viewed = True
                st.session_state.auth_mode = "register"
                st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # 2. MAIN HERO CARD CONTAINER (Pure HTML without comment blocks)
    st.markdown("""<div style="background: linear-gradient(135deg, #07192C 0%, #153B5E 50%, #1E4E7A 100%); border-radius: 24px; padding: 36px 40px; color: #FFFFFF; box-shadow: 0 20px 40px rgba(7, 25, 44, 0.22); margin-bottom: 20px;">
<div style="display: inline-block; background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 999px; padding: 5px 16px; font-size: 10.5px; font-weight: 800; color: #7DD3FC; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 22px;">REAL-TIME FRAUD DEFENSE SANDBOX &bull; V1.2</div>
<div style="font-size: 42px; font-weight: 800; color: #FFFDD0; line-height: 1.12; margin: 0 0 16px 0; letter-spacing: -0.03em; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">Secure payments.<br>Intelligent protection.</div>
<div style="font-size: 14.5px; color: #E2E8F0; line-height: 1.6; max-width: 740px; margin-bottom: 34px; font-weight: 400;">PayGuard merges consumer digital wallet simplicity with enterprise-grade neural anomaly detection. Every transaction is evaluated against behavioral baselines, device fingerprints, and ledger integrity within milliseconds.</div>
<div style="display: grid; grid-template-columns: 1fr 1.2fr 1.2fr 1.2fr; gap: 0; border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 20px;">
<div style="padding-right: 16px;">
<div style="font-size: 24px; font-weight: 800; color: #38BDF8; letter-spacing: -0.02em;">&lt; 50ms</div>
<div style="font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">MODEL LATENCY</div>
</div>
<div style="border-left: 1px solid rgba(255, 255, 255, 0.18); padding-left: 20px; padding-right: 16px;">
<div style="font-size: 24px; font-weight: 800; color: #38BDF8; letter-spacing: -0.02em;">3-Tier</div>
<div style="font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">ALLOW &bull; VERIFY &bull; REVIEW</div>
</div>
<div style="border-left: 1px solid rgba(255, 255, 255, 0.18); padding-left: 20px; padding-right: 16px;">
<div style="font-size: 24px; font-weight: 800; color: #38BDF8; letter-spacing: -0.02em;">256-Bit</div>
<div style="font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">LEDGER CONSISTENCY</div>
</div>
<div style="border-left: 1px solid rgba(255, 255, 255, 0.18); padding-left: 20px;">
<div style="font-size: 24px; font-weight: 800; color: #34D399; letter-spacing: -0.02em;">Zero Risk</div>
<div style="font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">INTERNAL SANDBOX DEMO</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    # 3. BOTTOM HERO ACTION BUTTONS
    col_b1, col_b2, _ = st.columns([1.2, 1.4, 1.4])
    with col_b1:
        if st.button("Sign In to Account →", type="primary", key="hero_btn_signin_acc", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "login"
            st.rerun()

    with col_b2:
        if st.button("📝 Register New Account →", key="hero_btn_register_acc", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "register"
            st.rerun()
