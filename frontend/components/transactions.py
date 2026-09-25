"""
PayGuard AI - Transaction History Screen Component.
Groups transactions by date and provides detailed security decision breakdown for each transfer.
"""

from collections import defaultdict
import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService
from frontend.styles.theme import render_status_pill, render_risk_gauge

def render_transaction_history():
    """Renders the client-facing Transaction History screen."""
    user = AuthService.get_current_user()
    if not user:
        st.session_state.current_screen = "login"
        st.rerun()
        return

    tx_service = MockTransactionService(user["user_id"])
    transactions = tx_service.get_transactions()

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">Transaction History</h1>
        <div style="font-size: 13px; color: #6B7280;">Audit trail of executed transfers and real-time security decisions.</div>
    </div>
    """, unsafe_allow_html=True)

    # Empty State Handling with real copy and layout
    if not transactions:
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 40px 16px;">
                <div style="width: 52px; height: 52px; border-radius: 50%; background: #EEF3FF; color: #2F5FDE; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 14px;">
                    📋
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                    No transactions yet
                </div>
                <div style="font-size: 13px; color: #6B7280; max-width: 360px; margin: 0 auto 20px auto;">
                    Your transaction history will record settled transfers, verification step-ups, and risk reviews.
                </div>
            </div>
            """, unsafe_allow_html=True)
            col_c, _ = st.columns([1, 2])
            with col_c:
                if st.button("Send Money Now →", type="primary", use_container_width=True):
                    st.session_state.current_screen = "send_money"
                    st.session_state.payment_step = "form"
                    st.rerun()
        return

    # Group transactions by date
    grouped = defaultdict(list)
    for tx in transactions:
        group_key = tx.get("date_group", "Recent Transfers")
        grouped[group_key].append(tx)

    for group_name, tx_list in grouped.items():
        st.markdown(f'<div style="font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin: 18px 0 8px 0;">{group_name}</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            for tx in tx_list:
                tx_id = tx.get("transaction_id")
                recipient = tx.get("recipient", "Unknown")
                amount = tx.get("amount", 0.0)
                status = tx.get("status", "Completed")
                time_str = tx.get("timestamp", "")[:19].replace("T", " ")
                decision = tx.get("decision", "ALLOW")
                score = tx.get("risk_score", 0)
                signals = tx.get("risk_signals", [])
                integrity = tx.get("transaction_integrity", {})

                # Summary Row
                st.markdown(f"""
                <div class="tx-row">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #EEF3FF; color: #2F5FDE; display: flex; align-items: center; justify-content: center; font-size: 14px;">
                            💳
                        </div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px; color: #0B1D33;">{recipient}</div>
                            <div style="font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">
                                ID: {tx_id} &bull; {time_str}
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="money-figure" style="font-size: 14px; font-weight: 600; color: #0B1D33;">
                            ₹ {amount:,.2f}
                        </div>
                        <div style="margin-top: 2px;">
                            {render_status_pill(status)}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Detail Sheet Accordion
                with st.expander(f"Security Details (ID: {tx_id})"):
                    d_col1, d_col2 = st.columns([1, 1.2])
                    with d_col1:
                        st.markdown(f"""
                        <div style="font-size: 12px; color: #6B7280; margin-bottom: 4px;">Engine Decision:</div>
                        <div style="margin-bottom: 10px;">{render_status_pill(decision)}</div>
                        <div style="font-size: 12px; color: #6B7280; margin-bottom: 2px;">Risk Score: <strong>{score} / 100</strong></div>
                        <div style="font-size: 12px; color: #6B7280; margin-bottom: 2px;">Fraud Probability: <strong>{tx.get('fraud_probability', 0.0) * 100:.1f}%</strong></div>
                        <div style="font-size: 11px; color: #6B7280; margin-top: 6px; font-family: 'JetBrains Mono', monospace;">
                            Engine: {tx.get('model_version', 'RXT-ResNeXt-GRU-v1.2')}
                        </div>
                        """, unsafe_allow_html=True)
                    with d_col2:
                        st.markdown('<div style="font-size: 12px; font-weight: 600; color: #0B1D33; margin-bottom: 6px;">Evaluated Signals:</div>', unsafe_allow_html=True)
                        if signals:
                            for s in signals:
                                st.markdown(f'<div style="font-size: 11px; color: #475569; padding: 2px 0;">• {s}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="font-size: 11px; color: #6B7280;">Standard low-risk transfer baseline</div>', unsafe_allow_html=True)

                        st.markdown('<div style="font-size: 12px; font-weight: 600; color: #0B1D33; margin: 8px 0 4px 0;">Ledger Integrity:</div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="font-size: 11px; color: #6B7280; font-family: 'JetBrains Mono', monospace;">
                            Sender Debited: {integrity.get('sender_debited', True)} &bull; Gateway: {integrity.get('gateway_status', 'SUCCESS')}
                        </div>
                        """, unsafe_allow_html=True)
