"""
PayGuard AI - User Profile Screen Component.
Displays customer information, wallet balance summary, and secure logout.
"""

import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService

def render_profile():
    """Renders the client-facing Profile screen."""
    user = AuthService.get_current_user()
    if not user:
        st.session_state.current_screen = "login"
        st.rerun()
        return

    tx_service = MockTransactionService(user["user_id"])
    balance = tx_service.get_balance()

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">User Profile</h1>
        <div style="font-size: 13px; color: #6B7280;">Account details, security settings, and session controls.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # Header with Avatar & Name
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px; padding-bottom: 20px; border-bottom: 1px solid #EDEFF3; margin-bottom: 20px;">
            <div style="width: 56px; height: 56px; border-radius: 50%; background: #2F5FDE; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 20px; box-shadow: 0 4px 12px rgba(47, 95, 222, 0.25);">
                {user.get('avatar_initials', 'U')}
            </div>
            <div>
                <div style="font-size: 18px; font-weight: 700; color: #0B1D33;">{user.get('name')}</div>
                <div style="font-size: 12px; color: #6B7280; margin-top: 2px;">Customer Identifier: {user.get('user_id')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Registered Mobile</div>
                <div style="font-size: 14px; font-weight: 600; color: #0B1D33; margin-top: 2px;">+91 {user.get('mobile')}</div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Virtual Payment Address (UPI)</div>
                <div style="font-size: 14px; font-weight: 600; color: #0B1D33; margin-top: 2px; font-family: 'JetBrains Mono', monospace;">{user.get('upi_id')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_info2:
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Wallet Account Number</div>
                <div style="font-size: 14px; font-weight: 600; color: #0B1D33; margin-top: 2px; font-family: 'JetBrains Mono', monospace;">{user.get('account_num')}</div>
            </div>
            <div style="margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Wallet Balance</div>
                <div class="money-figure" style="font-size: 18px; font-weight: 700; color: #1E9E6B; margin-top: 2px;">₹ {balance:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin: 16px 0; border-top: 1px solid #EDEFF3;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #F7F8FA; border-radius: 12px; padding: 14px 16px; margin-bottom: 20px;">
            <div style="font-size: 12px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">Security & Encryption Status</div>
            <div style="font-size: 12px; color: #6B7280; line-height: 1.5;">
                Your account is protected by real-time behavioral modeling, 256-bit ledger verification, and dynamic step-up challenge policies.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_rst, col_out = st.columns([1, 1])
        with col_rst:
            init_bal = float(user.get("initial_balance", 50000.0))
            if st.button(f"🔄 Reset Balance (₹{init_bal:,.0f})", use_container_width=True):
                st.session_state.wallet_balances[user["user_id"]] = init_bal
                try:
                    from backend.app.database import db_manager
                    conn = db_manager._get_sqlite_conn()
                    conn.execute("UPDATE users SET available_balance = ? WHERE user_id = ?", (init_bal, user["user_id"]))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
                st.success("Wallet balance reset.")
                st.rerun()

        with col_out:
            if st.button("🚪 Logout of Account", type="primary", use_container_width=True):
                AuthService.logout()
