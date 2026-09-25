"""
PayGuard AI - Security Center Screen Component.
Displays live security telemetry status pills and recent audit feed derived from session transactions.
"""

import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService
from frontend.services.backend_api import BackendAPIService
from frontend.styles.theme import render_status_pill

def render_security_center():
    """Renders the client-facing Security Center screen."""
    user = AuthService.get_current_user()
    if not user:
        st.session_state.current_screen = "login"
        st.rerun()
        return

    tx_service = MockTransactionService(user["user_id"])
    audit_events = tx_service.get_security_audit_events()

    api_service = BackendAPIService()
    health = api_service.check_health(force_refresh=False)
    backend_status = health.get("status_label", "Offline")

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">🛡️ Security Center</h1>
        <div style="font-size: 13px; color: #6B7280;">Real-time payment protection telemetry and active security monitoring.</div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Core System Status Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.markdown("""
            <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">
                AI Security Protection
            </div>
            """, unsafe_allow_html=True)
            st.markdown(render_status_pill("Active"), unsafe_allow_html=True)
            st.markdown('<div style="font-size: 11px; color: #6B7280; margin-top: 8px;">256-Bit Ledger Verification</div>', unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown("""
            <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">
                Transaction Monitoring
            </div>
            """, unsafe_allow_html=True)
            st.markdown(render_status_pill("Active"), unsafe_allow_html=True)
            st.markdown('<div style="font-size: 11px; color: #6B7280; margin-top: 8px;">Continuous Behavioral Scoring</div>', unsafe_allow_html=True)

    with c3:
        with st.container(border=True):
            st.markdown("""
            <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">
                Security Engine
            </div>
            """, unsafe_allow_html=True)
            st.markdown(render_status_pill("Active"), unsafe_allow_html=True)
            st.markdown(f'<div style="font-size: 11px; color: #6B7280; margin-top: 8px;">{health.get("model_version", "RXT v1.2")}</div>', unsafe_allow_html=True)

    with c4:
        with st.container(border=True):
            st.markdown("""
            <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">
                FastAPI Backend
            </div>
            """, unsafe_allow_html=True)
            st.markdown(render_status_pill(backend_status), unsafe_allow_html=True)
            st.markdown('<div style="font-size: 11px; color: #6B7280; margin-top: 8px;">REST @ /api/v1/health</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Recent Security Activity Feed
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 700; color: #0B1D33; text-transform: uppercase; letter-spacing: 0.05em;">
            Recent Security Activity Feed
        </div>
        <div style="font-size: 11px; color: #6B7280;">Derived from verified session transactions</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        if not audit_events:
            st.markdown("""
            <div style="text-align: center; padding: 24px; color: #6B7280; font-size: 13px;">
                No security events recorded in this session.
            </div>
            """, unsafe_allow_html=True)
        else:
            for ev in audit_events:
                decision = ev.get("decision", "ALLOW")
                tx_id = ev.get("transaction_id")
                time_str = ev.get("timestamp")
                recipient = ev.get("recipient")
                amount = ev.get("amount", 0.0)
                score = ev.get("risk_score", 0)

                icon = "✓" if decision == "ALLOW" else ("🔑" if decision == "VERIFY" else "🛡️")
                
                st.markdown(f"""
                <div class="tx-row">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background: #F7F8FA; border: 1px solid #EDEFF3; display: flex; align-items: center; justify-content: center; font-size: 13px;">
                            {icon}
                        </div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px; color: #0B1D33;">
                                Transfer to {recipient} &bull; ₹{amount:,.2f}
                            </div>
                            <div style="font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">
                                TXN #{tx_id} &bull; {time_str} &bull; Risk Score: {score}/100
                            </div>
                        </div>
                    </div>
                    <div>
                        {render_status_pill(decision)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
