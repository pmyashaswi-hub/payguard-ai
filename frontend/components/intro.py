"""
PayGuard AI - Introduction & Project Overview Webpage.
Serves as an elegant, professional fintech landing page before entering the sign-in screen.
"""

import streamlit as st
from frontend.services.backend_api import BackendAPIService
from frontend.styles.theme import render_status_pill

def render_intro():
    """Renders the comprehensive project introduction webpage with smooth transitions."""
    api_service = BackendAPIService()
    health = api_service.check_health(force_refresh=False)
    backend_status = health.get("status_label", "Offline")

    # Main Animated Container
    st.markdown('<div class="intro-container">', unsafe_allow_html=True)

    # 1. TOP NAVBAR
    col_nav_brand, col_nav_action = st.columns([1.1, 1.4])
    with col_nav_brand:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0 16px 0;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: #2F5FDE; display: flex; align-items: center; justify-content: center; color: #FFFFFF; font-size: 20px; font-weight: 800; box-shadow: 0 4px 12px rgba(47, 95, 222, 0.25);">
                🛡️
            </div>
            <div>
                <div style="font-weight: 800; font-size: 19px; color: #0B1D33; letter-spacing: -0.03em; line-height: 1.1;">
                    PayGuard
                </div>
                <div style="font-size: 11px; color: #6B7280; font-weight: 500;">
                    Intelligent Payment Protection
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_nav_action:
        c_status, c_nav_login, c_nav_reg = st.columns([1.2, 0.9, 1.1])
        with c_status:
            st.markdown(f"""
            <div style="padding-top: 8px; font-size: 11px; color: #6B7280; font-weight: 600;">
                Backend: {render_status_pill(backend_status)}
            </div>
            """, unsafe_allow_html=True)
        with c_nav_login:
            if st.button("Sign In", key="nav_btn_signin", use_container_width=True):
                st.session_state.intro_viewed = True
                st.session_state.auth_mode = "login"
                st.rerun()
        with c_nav_reg:
            if st.button("Register", type="primary", key="nav_btn_register", use_container_width=True):
                st.session_state.intro_viewed = True
                st.session_state.auth_mode = "register"
                st.rerun()

    # 2. HERO BANNER
    st.markdown("""
    <div class="intro-hero">
        <div class="intro-badge">
            <span class="pulse-dot"></span>
            <span>Real-Time Fraud Defense Sandbox &bull; v1.2</span>
        </div>
        <div style="margin: 0 0 18px 0; line-height: 1.15;">
            <div style="font-size: 42px; font-weight: 800; color: #FFFDD0; letter-spacing: -0.03em; text-shadow: 0 2px 12px rgba(0,0,0,0.4);">
                Secure payments.
            </div>
            <div style="font-size: 42px; font-weight: 800; color: #FFFDD0; letter-spacing: -0.03em; text-shadow: 0 0 28px rgba(0,0,0,0.5);">
                Intelligent protection.
            </div>
        </div>
        <div style="font-size: 15px; color: #E0E7FF; line-height: 1.6; max-width: 680px; margin-bottom: 28px; font-weight: 400;">
            PayGuard merges consumer digital wallet simplicity with enterprise-grade neural anomaly detection. Every transaction is evaluated against behavioral baselines, device fingerprints, and ledger integrity within milliseconds.
        </div>
        <div style="display: flex; gap: 24px; flex-wrap: wrap; margin-bottom: 8px;">
            <div>
                <div style="font-size: 22px; font-weight: 700; color: #67E8F9;">&lt; 50ms</div>
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Model Latency</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.15); padding-left: 20px;">
                <div style="font-size: 22px; font-weight: 700; color: #67E8F9;">3-Tier</div>
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">ALLOW &bull; VERIFY &bull; REVIEW</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.15); padding-left: 20px;">
                <div style="font-size: 22px; font-weight: 700; color: #67E8F9;">256-Bit</div>
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Ledger Consistency</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.15); padding-left: 20px;">
                <div style="font-size: 22px; font-weight: 700; color: #4ADE80;">Zero Risk</div>
                <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Internal Sandbox Demo</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Primary Enter CTA Buttons
    c_btn1, c_btn2, _ = st.columns([1.2, 1.4, 1.4])
    with c_btn1:
        if st.button("Sign In to Account →", type="primary", key="hero_btn_signin", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "login"
            st.rerun()
    with c_btn2:
        if st.button("📝 Register New Account →", key="hero_btn_register", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "register"
            st.rerun()

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # 3. CORE ARCHITECTURE PILLARS (3 Cards)
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 20px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">
            Engineered for Modern Payment Risk
        </h2>
        <div style="font-size: 13px; color: #6B7280;">
            A three-tier defense model protecting account holders without introducing unnecessary friction.
        </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="intro-feature-card">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: #EEF3FF; color: #2F5FDE; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 14px;">
                🧠
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                ResNeXt-GRU Neural Scoring
            </div>
            <div style="font-size: 12px; color: #475569; line-height: 1.5;">
                PyTorch model evaluating normalized 16-dimensional feature vectors including spending surges, velocity in sliding windows, and temporal anomalies in sub-50ms.
            </div>
            <div style="margin-top: 14px; font-size: 11px; font-weight: 600; color: #2F5FDE;">
                Real-Time Inference &bull; Model v1.2
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="intro-feature-card">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: #E7F8F0; color: #1E9E6B; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 14px;">
                🛡️
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                Adaptive Decision Tiers
            </div>
            <div style="font-size: 12px; color: #475569; line-height: 1.5;">
                Transactions dynamically route to <strong>ALLOW</strong> (instant pass), <strong>VERIFY</strong> (step-up OTP challenge), or <strong>REVIEW</strong> (hard freeze for account compromise protection).
            </div>
            <div style="margin-top: 14px; font-size: 11px; font-weight: 600; color: #1E9E6B;">
                Zero-Friction Baseline
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="intro-feature-card">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: #EDEFF3; color: #6B7280; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 14px;">
                ⚖️
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                Ledger Reconciliation Guard
            </div>
            <div style="font-size: 12px; color: #475569; line-height: 1.5;">
                Double-entry validation checks consistency between gateway statuses and receiver credits. Flags reconciliation requirements neutrally without mislabeling them as fraud.
            </div>
            <div style="margin-top: 14px; font-size: 11px; font-weight: 600; color: #6B7280;">
                Integrity Consistency Guard
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # 4. HOW IT WORKS TIMELINE (4 Steps)
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="font-size: 20px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">
            Lifecycle of a Protected Payment
        </h2>
        <div style="font-size: 13px; color: #6B7280;">
            How PayGuard analyzes and safeguards every transfer in real-time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 12px 4px;">
            <div>
                <div style="font-size: 12px; font-weight: 800; color: #2F5FDE; margin-bottom: 4px;">STEP 01</div>
                <div style="font-size: 13px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Initiate Transfer</div>
                <div style="font-size: 11px; color: #6B7280; line-height: 1.5;">
                    User selects recipient and transfer amount from available balance.
                </div>
            </div>
            <div>
                <div style="font-size: 12px; font-weight: 800; color: #2F5FDE; margin-bottom: 4px;">STEP 02</div>
                <div style="font-size: 13px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Signal Extraction</div>
                <div style="font-size: 11px; color: #6B7280; line-height: 1.5;">
                    Device fingerprint, subnet, velocity flags, and integrity flags assembled.
                </div>
            </div>
            <div>
                <div style="font-size: 12px; font-weight: 800; color: #2F5FDE; margin-bottom: 4px;">STEP 03</div>
                <div style="font-size: 13px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Neural Risk Scoring</div>
                <div style="font-size: 11px; color: #6B7280; line-height: 1.5;">
                    FastAPI model computes fraud probability and composite risk score (0-100).
                </div>
            </div>
            <div>
                <div style="font-size: 12px; font-weight: 800; color: #2F5FDE; margin-bottom: 4px;">STEP 04</div>
                <div style="font-size: 13px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Tiered Execution</div>
                <div style="font-size: 11px; color: #6B7280; line-height: 1.5;">
                    Instant settlement, 2FA step-up verification, or protective hold.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # 5. REVIEWER TESTING GUIDE
    with st.container(border=True):
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 700; color: #0B1D33; text-transform: uppercase;">
                🧑‍💼 Reviewer & Evaluator Sandbox Guide
            </div>
            <div style="font-size: 11px; color: #2F5FDE; font-weight: 600;">For HR, Mentors & Engineers</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 12px; color: #475569;">
            <div style="background: #F7F8FA; border-radius: 8px; padding: 12px;">
                <div style="font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Demo Accounts:</div>
                <div>&bull; <strong>Rahul Kumar</strong>: <code>9876543210</code> &bull; PIN: <code>1234</code></div>
                <div>&bull; <strong>Ananya Sharma</strong>: <code>9123456780</code> &bull; PIN: <code>5678</code></div>
            </div>
            <div style="background: #F7F8FA; border-radius: 8px; padding: 12px;">
                <div style="font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Scenario Testing:</div>
                <div>Use the <strong>Demo Scenario Flags</strong> inside the Send Money form to naturally trigger ALLOW, VERIFY (OTP <code>1234</code>), REVIEW, or Reconciliation decisions.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # 6. BOTTOM CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0B1D33 0%, #152E52 100%); border-radius: 16px; padding: 28px; text-align: center; color: #FFFFFF;">
        <div style="font-size: 18px; font-weight: 700; margin-bottom: 6px;">Ready to test PayGuard?</div>
        <div style="font-size: 13px; color: #94A3B8; max-width: 480px; margin: 0 auto 18px auto;">
            Enter the sandbox to experience seamless digital banking protected by real-time behavioral neural modeling.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_bot1, c_bot2, _ = st.columns([1.2, 1.3, 1.5])
    with c_bot1:
        if st.button("Sign In to Account →", type="primary", key="bottom_btn_signin", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "login"
            st.rerun()
    with c_bot2:
        if st.button("📝 Register New Account →", key="bottom_btn_register", use_container_width=True):
            st.session_state.intro_viewed = True
            st.session_state.auth_mode = "register"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # Close intro-container
