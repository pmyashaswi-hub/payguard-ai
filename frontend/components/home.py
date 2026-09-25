"""
PayGuard AI - Home & Wallet Dashboard Screen.
Renders wallet balance card, quick actions grid, and recent transaction preview.
"""

import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService
from frontend.services.backend_api import BackendAPIService
from frontend.styles.theme import render_money_text, render_status_pill

def render_home():
    """Renders the client-facing Home / Wallet screen."""
    user = AuthService.get_current_user()
    if not user:
        st.session_state.current_screen = "login"
        st.rerun()
        return

    tx_service = MockTransactionService(user["user_id"])
    balance = tx_service.get_balance()
    recent_txs = tx_service.get_transactions()[:3]

    api_service = BackendAPIService()
    health = api_service.check_health(force_refresh=False)
    health_label = health.get("status_label", "Offline")

    # Welcome Header
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">Welcome, {user.get('name', 'User')}</h1>
        <div style="font-size: 13px; color: #6B7280;">PayGuard Digital Wallet Account &bull; {user.get('account_num', '')}</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Main Wallet Balance Card
    st.markdown(f"""
    <div class="pg-card" style="background: linear-gradient(135deg, #0B1D33 0%, #152E52 100%); color: #FFFFFF; border: none; padding: 28px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
            <div>
                <div style="font-size: 11px; font-weight: 700; color: #90E0EF; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                    Available Wallet Balance
                </div>
                <div class="money-figure count-up-text" style="font-size: 36px; font-weight: 700; color: #FFFFFF; line-height: 1.1;">
                    <span style="font-size: 0.75em; opacity: 0.85; margin-right: 4px;">₹</span>{balance:,.2f}
                </div>
                <div style="font-size: 12px; color: #CBD5E1; margin-top: 8px; display: flex; align-items: center; gap: 6px;">
                    <span>🛡️</span>
                    <span>Protected by PayGuard AI &bull; 256-Bit Ledger Verification</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="display: inline-block; background: rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; color: #E0F2FE;">
                    Backend: {render_status_pill(health_label)}
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 8px; font-family: 'JetBrains Mono', monospace;">
                    UPI ID: {user.get('upi_id', '')}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Quick Actions Grid
    st.markdown('<div style="font-size: 13px; font-weight: 700; color: #0B1D33; text-transform: uppercase; letter-spacing: 0.05em; margin: 24px 0 12px 0;">Quick Actions</div>', unsafe_allow_html=True)
    
    qa_c1, qa_c2, qa_c3, qa_c4 = st.columns(4)

    with qa_c1:
        if st.button("💸 Send Money", type="primary", use_container_width=True):
            st.session_state.current_screen = "send_money"
            st.rerun()

    with qa_c2:
        st.button("📥 Request Money", disabled=True, help="Coming soon in next release", use_container_width=True)

    with qa_c3:
        st.button("📷 Scan & Pay", disabled=True, help="Coming soon in next release", use_container_width=True)

    with qa_c4:
        if st.button("📋 Transactions", use_container_width=True):
            st.session_state.current_screen = "transactions"
            st.rerun()

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # 3. Recent Activity Preview (3 rows)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div style="font-size: 13px; font-weight: 700; color: #0B1D33; text-transform: uppercase; letter-spacing: 0.05em;">
            Recent Activity Preview
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        if not recent_txs:
            st.markdown("""
            <div style="text-align: center; padding: 24px 0; color: #6B7280; font-size: 13px;">
                No recent transactions found. Tap <strong>Send Money</strong> to initiate your first transfer.
            </div>
            """, unsafe_allow_html=True)
        else:
            for tx in recent_txs:
                decision = tx.get("decision", "ALLOW")
                status = tx.get("status", "Completed")
                time_str = tx.get("timestamp", "")[:16].replace("T", " ")
                
                st.markdown(f"""
                <div class="tx-row">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #EEF3FF; color: #2F5FDE; display: flex; align-items: center; justify-content: center; font-size: 14px;">
                            💳
                        </div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px; color: #0B1D33;">{tx.get('recipient')}</div>
                            <div style="font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">{time_str}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="money-figure" style="font-size: 14px; font-weight: 600; color: #0B1D33;">
                            ₹ {tx.get('amount', 0.0):,.2f}
                        </div>
                        <div style="margin-top: 2px;">
                            {render_status_pill(status)}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col_all, _ = st.columns([1, 2])
            with col_all:
                if st.button("View Full Transaction History →", use_container_width=True):
                    st.session_state.current_screen = "transactions"
                    st.rerun()
