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
                <div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Linked Email / Firebase Google Auth</div>
                <div style="font-size: 13px; font-weight: 600; color: #001D39; margin-top: 2px;">
                    {user.get('email', 'N/A')}
                    <span style="display: inline-block; background: #FFF4E5; color: #D97706; border: 1px solid #F59E0B; font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 999px; margin-left: 6px;">
                        🔥 Firebase Verified
                    </span>
                </div>
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

        col_topup, col_out = st.columns([1, 1])
        with col_topup:
            with st.expander("💳 Top Up Wallet Balance", expanded=False):
                st.markdown("<div style='font-size: 13px; font-weight: 600; color: #0B1D33; margin-bottom: 8px;'>Add funds to your account:</div>", unsafe_allow_html=True)
                
                c_p1, c_p2, c_p3 = st.columns(3)
                p_amt = 0.0
                if c_p1.button("+₹1,000", key="p1k", use_container_width=True):
                    p_amt = 1000.0
                if c_p2.button("+₹5,000", key="p5k", use_container_width=True):
                    p_amt = 5000.0
                if c_p3.button("+₹10,000", key="p10k", use_container_width=True):
                    p_amt = 10000.0

                topup_custom = st.number_input(
                    "Or custom top up amount (₹):",
                    min_value=100.0,
                    max_value=1000000.0,
                    value=p_amt if p_amt > 0 else 5000.0,
                    step=500.0,
                    key="topup_custom_val"
                )

                if st.button("⚡ Add Money to Wallet", type="primary", use_container_width=True, key="btn_confirm_topup"):
                    amount_to_add = p_amt if p_amt > 0 else topup_custom
                    if amount_to_add > 0:
                        new_balance = tx_service.top_up_balance(amount_to_add)
                        st.success(f"✅ Successfully added ₹{amount_to_add:,.2f}! New Balance: ₹{new_balance:,.2f}")
                        st.rerun()

        with col_out:
            if st.button("🚪 Logout of Account", use_container_width=True):
                AuthService.logout()

