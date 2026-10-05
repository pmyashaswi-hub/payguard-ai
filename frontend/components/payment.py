"""
PayGuard AI - Send Money, Payment Review, Security Check, Decision & Success Screens.
Implements complete client-facing payment lifecycle adhering strictly to the backend contract.
"""

import time
import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.mock_transaction_service import MockTransactionService
from frontend.services.backend_api import BackendAPIService
from frontend.services.clerk_service import ClerkAuthService
from frontend.styles.theme import (
    render_money_text,
    render_status_pill,
    render_risk_gauge,
    render_signal_chip,
    NAVY_900,
    BLUE_600,
    SUCCESS_600,
    AMBER_600,
    DANGER_600,
    NEUTRAL_500
)

def render_payment_flow():
    """Renders the step-by-step payment flow."""
    user = AuthService.get_current_user()
    if not user:
        st.session_state.current_screen = "login"
        st.rerun()
        return

    tx_service = MockTransactionService(user["user_id"])
    balance = tx_service.get_balance()

    if "payment_step" not in st.session_state:
        st.session_state.payment_step = "form"

    # Screen step router
    step = st.session_state.payment_step

    if step == "form":
        _render_payment_form(user, balance, tx_service)
    elif step == "review":
        _render_payment_review(user, balance)
    elif step == "security_check":
        _render_security_check(user, tx_service)
    elif step == "decision":
        _render_decision_screen(user, balance, tx_service)
    elif step == "success":
        _render_success_screen(user, balance)

# =========================================================================
# 1. SEND MONEY FORM
# =========================================================================
def _render_payment_form(user: dict, balance: float, tx_service: MockTransactionService):
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">Send Money</h1>
        <div style="font-size: 13px; color: #6B7280;">Transfer funds securely to any UPI ID, Mobile number, or Bank Account.</div>
    </div>
    """, unsafe_allow_html=True)

    # Saved form draft preservation
    draft = st.session_state.get("payment_draft", {})
    recipient_val = draft.get("recipient", "")
    amount_val = float(draft.get("amount", 1500.0))
    note_val = draft.get("note", "Personal transfer")

    # Frequent Payees quick tap
    payees = tx_service.get_frequent_payees()
    if payees:
        st.markdown('<div style="font-size: 12px; font-weight: 700; color: #0B1D33; text-transform: uppercase; margin-bottom: 8px;">Frequent Payees</div>', unsafe_allow_html=True)
        cols = st.columns(len(payees))
        for idx, p in enumerate(payees):
            with cols[idx]:
                if st.button(f"{p['avatar']} {p['name']}", key=f"payee_btn_{idx}", use_container_width=True):
                    recipient_val = p["identifier"]
                    st.session_state["frequent_selected"] = recipient_val
    else:
        st.markdown("""
        <div style="font-size: 11.5px; color: #64748B; font-style: italic; margin-bottom: 8px;">
            ℹ️ No frequent payees saved yet. Completing a transfer will automatically save payees here.
        </div>
        """, unsafe_allow_html=True)

    if "frequent_selected" in st.session_state:
        recipient_val = st.session_state.pop("frequent_selected")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 12px; margin-bottom: 14px; border-bottom: 1px solid #EDEFF3;">
            <div style="font-size: 13px; color: #6B7280;">Debiting From: <strong>{user.get('account_num')}</strong></div>
            <div style="font-size: 13px; color: #0B1D33; font-weight: 600;">Available: ₹{balance:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        recipient_input = st.text_input(
            "Recipient UPI ID / Mobile / Account Number",
            value=recipient_val,
            placeholder="e.g. priya.s@upi or 9876543210",
            key="input_pay_recipient"
        )

        amount_input = st.number_input(
            "Transfer Amount (₹)",
            min_value=1.0,
            max_value=10000000.0,
            value=min(amount_val, 100000.0),
            step=100.0,
            format="%.2f",
            help="Maximum transfer limit per transaction is ₹1,00,000 (1 Lakh).",
            key="input_pay_amount"
        )

        note_input = st.text_input(
            "Payment Purpose / Note (Optional)",
            value=note_val,
            placeholder="e.g. Dinner share, Rent, Utilities",
            key="input_pay_note"
        )

        # Demo Test Scenario Flags for reviewers (HR / mentor / engineers)
        with st.expander("🛠️ Demo Scenario Flags (For Reviewers to test engine decisions)"):
            st.markdown("""
            <div style="font-size: 11px; color: #6B7280; margin-bottom: 8px;">
                These flags populate real behavioral metadata sent directly to the FastAPI <code>/predict</code> engine.
            </div>
            """, unsafe_allow_html=True)
            c_s1, c_s2 = st.columns(2)
            with c_s1:
                flag_new_device = st.checkbox("New Device Fingerprint", value=draft.get("is_new_device", False))
                flag_new_location = st.checkbox("New Location / IP Subnet", value=draft.get("is_new_location", False))
            with c_s2:
                flag_high_velocity = st.checkbox("High Velocity Rapid Transfers", value=draft.get("high_velocity", False))
                flag_integrity_mismatch = st.checkbox("Simulate Ledger Mismatch (Reconciliation)", value=draft.get("integrity_mismatch", False))

        # Transaction limit & Balance check validation warnings
        if amount_input > 100000.0:
            st.markdown("""
            <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 10px 14px; font-size: 13px; font-weight: 700; margin-top: 10px;">
                ⚠️ You cannot send money more than 1 Lakh (₹1,00,000).
            </div>
            """, unsafe_allow_html=True)
        elif amount_input > balance:
            st.markdown("""
            <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600; margin-top: 10px;">
                ⚠️ Insufficient wallet balance for this transfer amount.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("Review Payment →", type="primary", use_container_width=True):
            if not recipient_input.strip():
                st.error("Please enter a valid recipient UPI ID, Mobile number, or Account.")
                return
            if amount_input > 100000.0:
                st.error("⚠️ You cannot send money more than 1 Lakh (₹1,00,000).")
                return
            if amount_input > balance:
                st.error("Transfer amount exceeds available wallet balance.")
                return

            st.session_state.payment_draft = {
                "recipient": recipient_input.strip(),
                "amount": float(amount_input),
                "note": note_input.strip(),
                "is_new_device": flag_new_device,
                "is_new_location": flag_new_location,
                "high_velocity": flag_high_velocity,
                "integrity_mismatch": flag_integrity_mismatch
            }
            st.session_state.payment_step = "review"
            st.rerun()

# =========================================================================
# 2. PAYMENT REVIEW SUMMARY CARD
# =========================================================================
def _render_payment_review(user: dict, balance: float):
    draft = st.session_state.get("payment_draft", {})
    if not draft:
        st.session_state.payment_step = "form"
        st.rerun()
        return

    amount = draft.get("amount", 0.0)
    recipient = draft.get("recipient", "")
    note = draft.get("note", "Personal transfer")
    balance_after = balance - amount

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">Payment Review</h1>
        <div style="font-size: 13px; color: #6B7280;">Please verify transfer details before triggering security analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0; border-bottom: 1px solid #EDEFF3; margin-bottom: 18px;">
            <div style="font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase;">Amount to Transfer</div>
            <div class="money-figure" style="font-size: 34px; font-weight: 700; color: #0B1D33; margin-top: 4px;">
                ₹ {amount:,.2f}
            </div>
            <div style="font-size: 11px; color: #1E9E6B; font-weight: 600; margin-top: 4px;">Zero Platform Fees</div>
        </div>

        <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 13px; border-bottom: 1px solid #EDEFF3;">
            <span style="color: #6B7280;">Recipient</span>
            <span style="font-weight: 600; color: #0B1D33;">{recipient}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 13px; border-bottom: 1px solid #EDEFF3;">
            <span style="color: #6B7280;">Debited Account</span>
            <span style="font-weight: 600; color: #0B1D33;">{user.get('account_num')}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 13px; border-bottom: 1px solid #EDEFF3;">
            <span style="color: #6B7280;">Note</span>
            <span style="font-weight: 500; color: #0B1D33;">{note or 'N/A'}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 13px;">
            <span style="color: #6B7280;">Balance After Transfer</span>
            <span style="font-weight: 600; color: #0B1D33;">₹ {balance_after:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #F0F6FA; border: 1px solid #BDD8E9; border-radius: 10px; padding: 12px 14px; margin-bottom: 12px;">
            <div style="font-size: 12px; font-weight: 700; color: #001D39;">🔒 Authorize Transaction with UPI PIN</div>
            <div style="font-size: 11px; color: #49769F;">Please enter your registered 4-digit UPI PIN to authorize this transfer.</div>
        </div>
        """, unsafe_allow_html=True)

        entered_upi_pin = st.text_input(
            "Enter 4-Digit UPI PIN",
            type="password",
            max_chars=4,
            placeholder="••••",
            key="input_pay_upi_pin"
        )

        if "upi_pin_error" in st.session_state and st.session_state.upi_pin_error:
            st.markdown(f"""
            <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 10px 14px; font-size: 13px; font-weight: 700; margin-bottom: 12px;">
                ⚠️ {st.session_state.upi_pin_error}
            </div>
            """, unsafe_allow_html=True)

        col_edit, col_proceed = st.columns([1, 1.6])
        with col_edit:
            if st.button("← Edit Details", use_container_width=True):
                st.session_state.upi_pin_error = None
                st.session_state.payment_step = "form"
                st.rerun()

        with col_proceed:
            if st.button("Proceed to Security Check 🔒", type="primary", use_container_width=True):
                is_valid_pin = AuthService.verify_upi_pin(user["user_id"], entered_upi_pin)
                if not is_valid_pin:
                    st.session_state.upi_pin_error = "Please give the correct UPI pin."
                    st.rerun()
                else:
                    st.session_state.upi_pin_error = None
                    st.session_state.payment_step = "security_check"
                    st.rerun()

# =========================================================================
# 3. SECURITY CHECK SCREEN
# =========================================================================
def _render_security_check(user: dict, tx_service: MockTransactionService):
    draft = st.session_state.get("payment_draft", {})
    if not draft:
        st.session_state.payment_step = "form"
        st.rerun()
        return

    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">🛡️ Security Check</h1>
        <div style="font-size: 13px; color: #6B7280;">Real-time payment risk evaluation powered by PayGuard AI.</div>
    </div>
    """, unsafe_allow_html=True)

    status_placeholder = st.empty()

    # Generate or reuse unique transaction ID
    if "current_tx_id" not in st.session_state:
        st.session_state.current_tx_id = int(time.time() * 1000)

    tx_id = st.session_state.current_tx_id
    api_service = BackendAPIService()

    # Build canonical request payload via adapter
    integrity_mismatch = draft.get("integrity_mismatch", False)
    payload = api_service.build_transaction_payload(
        transaction_id=tx_id,
        user_id=user["user_id"],
        amount=draft.get("amount", 0.0),
        is_new_device=draft.get("is_new_device", False),
        is_new_location=draft.get("is_new_location", False),
        high_velocity=draft.get("high_velocity", False),
        receiver_credited=False if integrity_mismatch else True,
        gateway_status="SUCCESS" if not integrity_mismatch else "SUCCESS"
    )

    with status_placeholder.container():
        with st.container(border=True):
            st.markdown("""
            <div style="text-align: center; padding: 24px 0;">
                <div style="font-size: 14px; font-weight: 600; color: #0B1D33; margin-bottom: 16px;">
                    Executing Multi-Layer Risk Verification...
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Connecting to FastAPI Security Engine (/api/v1/predict)..."):
                success, response_data, error_msg = api_service.predict_risk(payload)

    if not success:
        # Network / Backend failure state
        with status_placeholder.container():
            with st.container(border=True):
                st.markdown(f"""
                <div style="text-align: center; padding: 24px 16px;">
                    <div style="width: 48px; height: 48px; border-radius: 50%; background: #FDECEA; color: #C0392B; display: inline-flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 12px;">
                        ⚠️
                    </div>
                    <div style="font-size: 16px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                        Security analysis is currently unavailable
                    </div>
                    <div style="font-size: 13px; color: #6B7280; max-width: 420px; margin: 0 auto 18px auto;">
                        {error_msg or "Please verify the FastAPI backend server is running and try again."}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_retry, col_cancel = st.columns([1, 1])
                with col_retry:
                    if st.button("🔄 Retry Analysis", type="primary", use_container_width=True):
                        st.session_state.current_tx_id = int(time.time() * 1000)
                        st.rerun()
                with col_cancel:
                    if st.button("Cancel & Return to Form", use_container_width=True):
                        st.session_state.payment_step = "form"
                        st.rerun()
        return

    # If successful, show sequential checklist reveal driven by the resolved lifecycle
    with status_placeholder.container():
        with st.container(border=True):
            st.markdown("""
            <div style="padding: 10px 0 16px 0;">
                <div style="font-size: 12px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 12px;">
                    Verification Pipeline Checklist
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <div style="font-size: 13px; color: #1E9E6B; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                        <span>✓</span> <span>Transaction Details & Payload Integrity Verified</span>
                    </div>
                    <div style="font-size: 13px; color: #1E9E6B; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                        <span>✓</span> <span>Device Fingerprint & Subnet Signals Assessed</span>
                    </div>
                    <div style="font-size: 13px; color: #1E9E6B; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                        <span>✓</span> <span>Temporal Behavior & Velocity Patterns Evaluated</span>
                    </div>
                    <div style="font-size: 13px; color: #1E9E6B; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                        <span>✓</span> <span>RXT Neural Anomaly Model Decision Formulated</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Save parsed response into session_state and progress to decision
    st.session_state.security_result = response_data
    st.session_state.payment_step = "decision"
    st.rerun()

# =========================================================================
# 4. DECISION SCREENS (ALLOW / VERIFY / REVIEW / RECONCILIATION)
# =========================================================================
def _render_decision_screen(user: dict, balance: float, tx_service: MockTransactionService):
    draft = st.session_state.get("payment_draft", {})
    result = st.session_state.get("security_result", {})
    if not draft or not result:
        st.session_state.payment_step = "form"
        st.rerun()
        return

    decision = result.get("decision", "ALLOW")
    reconciliation = result.get("reconciliation_required", False)
    score = result.get("risk_score", 0)
    signals = result.get("risk_signals", [])
    amount = draft.get("amount", 0.0)
    recipient = draft.get("recipient", "")
    tx_id = st.session_state.get("current_tx_id", int(time.time() * 1000))

    # Header
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="font-size: 24px; font-weight: 700; color: #0B1D33; margin: 0 0 4px 0;">Security Decision</h1>
        <div style="font-size: 13px; color: #6B7280;">Real-time risk scoring and payment authorization status.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # 4A. RECONCILIATION REQUIRED STATE (Distinct neutral-500 styling, never labeled fraud)
        if reconciliation:
            # Real-time logging of Reconciliation Required state into Transaction History & SQLite DB
            if not st.session_state.get("logged_reconciliation_tx"):
                tx_service.record_completed_transaction(
                    transaction_id=tx_id,
                    recipient=recipient,
                    recipient_id=recipient,
                    amount=amount,
                    prediction_result=result,
                    deduct_balance=False
                )
                st.session_state.logged_reconciliation_tx = True

            st.markdown(f"""
            <div style="text-align: center; padding: 10px 0;">
                <div class="decision-circle reconciliation">
                    <span style="font-size: 28px;">⚖️</span>
                </div>
                <div style="font-size: 18px; font-weight: 700; color: #0B1D33; margin-bottom: 4px;">
                    Reconciliation Required
                </div>
                <div style="font-size: 13px; color: #6B7280; max-width: 440px; margin: 0 auto 16px auto;">
                    A ledger state inconsistency was detected between the payment gateway and settlement ledger. Transaction paused for reconciliation.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(render_risk_gauge(score, "RECONCILIATION"), unsafe_allow_html=True)

            col_home, col_detail = st.columns([1, 1])
            with col_home:
                if st.button("Back to Home", type="primary", use_container_width=True):
                    st.session_state.pop("logged_reconciliation_tx", None)
                    st.session_state.current_screen = "home"
                    st.session_state.payment_step = "form"
                    st.rerun()
            with col_detail:
                with st.expander("Technical Audit Details"):
                    st.json(result.get("raw_response", {}))
            return

        # 4B. REVIEW STATE (High Risk, Blocked, No path to completion)
        if decision == "REVIEW":
            st.markdown(f"""
            <div style="text-align: center; padding: 10px 0;">
                <div class="decision-circle review">
                    <span style="font-size: 28px;">🛡️</span>
                </div>
                <div style="font-size: 18px; font-weight: 700; color: #C0392B; margin-bottom: 4px;">
                    Payment Requires Security Review
                </div>
                <div style="font-size: 13px; color: #6B7280; max-width: 440px; margin: 0 auto 16px auto;">
                    This transaction triggered elevated risk patterns and has been held by PayGuard AI protection rules. Funds have not been debited.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(render_risk_gauge(score, "REVIEW"), unsafe_allow_html=True)

            # Plainly display detected signals
            st.markdown('<div style="font-size: 12px; font-weight: 700; color: #0B1D33; text-transform: uppercase; margin: 12px 0 8px 0;">Risk Signals Evaluated:</div>', unsafe_allow_html=True)
            for sig in signals:
                st.markdown(f"""
                <div style="font-size: 12px; color: #C0392B; background: #FDECEA; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; font-weight: 500;">
                    • {sig}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            # Log reviewed transaction in history for audit
            if not st.session_state.get("logged_review_tx"):
                tx_service.record_completed_transaction(
                    transaction_id=tx_id,
                    recipient=recipient,
                    recipient_id=recipient,
                    amount=amount,
                    prediction_result=result
                )
                st.session_state.logged_review_tx = True

            col_home, col_detail = st.columns([1, 1])
            with col_home:
                if st.button("Back to Home", type="primary", use_container_width=True):
                    st.session_state.pop("logged_review_tx", None)
                    st.session_state.current_screen = "home"
                    st.session_state.payment_step = "form"
                    st.rerun()
            with col_detail:
                with st.expander("Technical Security Audit"):
                    st.json(result.get("raw_response", {}))
            return

        # 4C. VERIFY STATE (Risk score 26 to 65: Step-Up Real-Time Email OTP Verification required)
        if decision == "VERIFY":
            user_email = user.get("email", "").strip().lower()

            # Auto-trigger real-time Clerk / SMTP email OTP dispatch for this transaction
            if st.session_state.get("step_up_otp_tx_id") != tx_id:
                if user_email:
                    sent_ok, msg, code_gen = ClerkAuthService.send_email_code(user_email)
                    st.session_state.step_up_otp_tx_id = tx_id
                    st.session_state.step_up_otp_status = msg
                    st.session_state.step_up_otp_sent_to = user_email
                else:
                    st.session_state.step_up_otp_tx_id = tx_id
                    st.session_state.step_up_otp_status = "No email address registered for active user profile."
                    st.session_state.step_up_otp_sent_to = "N/A"

            st.markdown(f"""
            <div style="text-align: center; padding: 10px 0;">
                <div class="decision-circle verify">
                    <span style="font-size: 28px;">🔑</span>
                </div>
                <div style="font-size: 18px; font-weight: 700; color: #B7791F; margin-bottom: 4px;">
                    Additional Verification Required
                </div>
                <div style="font-size: 13px; color: #6B7280; max-width: 440px; margin: 0 auto 12px auto;">
                    Fraud risk score ({score}/100) is between 26 and 65. Secondary real-time email verification code required to confirm this transaction.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(render_risk_gauge(score, "VERIFY"), unsafe_allow_html=True)

            # Signal chips
            st.markdown('<div style="font-size: 12px; font-weight: 700; color: #0B1D33; text-transform: uppercase; margin-bottom: 8px;">Triggering Indicators:</div>', unsafe_allow_html=True)
            for sig in signals:
                st.markdown(f"""
                <div style="font-size: 12px; color: #B7791F; background: #FFF6E5; padding: 6px 12px; border-radius: 8px; margin-bottom: 6px;">
                    • {sig}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # Real-Time Email Verification Banner
            status_msg = st.session_state.get("step_up_otp_status", "")
            sent_email = st.session_state.get("step_up_otp_sent_to", user_email)

            st.markdown(f"""
            <div style="background: #F0F6FA; border: 1px solid #BDD8E9; border-radius: 12px; padding: 16px; margin-bottom: 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #001D39; text-transform: uppercase; margin-bottom: 4px;">
                    ✉️ Real-Time Email Verification Sent
                </div>
                <div style="font-size: 12.5px; color: #0A4174; font-weight: 600; margin-bottom: 4px;">
                    Verification code dispatched to: <span style="color: #001D39;">{sent_email}</span>
                </div>
                <div style="font-size: 11px; color: #49769F;">
                    {status_msg}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_otp_in, col_resend = st.columns([2.2, 1])
            with col_otp_in:
                otp_input = st.text_input(
                    "Enter Verification Code",
                    placeholder="Enter code sent to mail or 424242",
                    key="input_verify_otp"
                )
            with col_resend:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("Resend Code", use_container_width=True):
                    if user_email:
                        sent_ok, msg, code_gen = ClerkAuthService.send_email_code(user_email)
                        st.session_state.step_up_otp_status = f"🔄 New code sent to {user_email}!"
                        st.session_state.otp_error = None
                        st.toast(f"Verification code resent to {user_email}!")
                        st.rerun()

            if "otp_error" in st.session_state and st.session_state.otp_error:
                st.markdown(f"""
                <div style="color: #C0392B; font-size: 12px; font-weight: 600; margin-bottom: 8px;">
                    ⚠️ {st.session_state.otp_error}
                </div>
                """, unsafe_allow_html=True)

            col_sub_otp, col_can_otp = st.columns([1.4, 1])
            with col_sub_otp:
                if st.button("Confirm Verification & Pay ₹{:,.2f}".format(amount), type="primary", use_container_width=True):
                    entered_code = otp_input.strip()
                    is_valid = False
                    verify_reason = ""

                    if user_email and entered_code:
                        is_valid, verify_reason = ClerkAuthService.verify_email_code(user_email, entered_code)

                    # Developer test fallbacks
                    if not is_valid and entered_code in ["1234", "424242", "123456"]:
                        is_valid = True

                    if is_valid:
                        st.session_state.otp_error = None
                        success = tx_service.record_completed_transaction(
                            transaction_id=tx_id,
                            recipient=recipient,
                            recipient_id=recipient,
                            amount=amount,
                            prediction_result=result
                        )
                        if success:
                            st.session_state.payment_step = "success"
                            st.rerun()
                        else:
                            st.session_state.otp_error = "Insufficient wallet balance."
                            st.rerun()
                    else:
                        st.session_state.otp_error = f"Invalid verification code. Check inbox ({user_email}) or enter test code 424242."
                        st.rerun()

            with col_can_otp:
                if st.button("Cancel Payment", use_container_width=True):
                    st.session_state.payment_step = "form"
                    st.rerun()
            return

        # 4D. ALLOW STATE (Authorized, User May Confirm & Pay)
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0;">
            <div class="decision-circle allow">
                <span style="font-size: 28px;">✓</span>
            </div>
            <div style="font-size: 18px; font-weight: 700; color: #1E9E6B; margin-bottom: 4px;">
                Transaction Authorized
            </div>
            <div style="font-size: 13px; color: #6B7280; max-width: 440px; margin: 0 auto 12px auto;">
                PayGuard AI risk evaluation passed all security checks. You may now confirm and execute transfer.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(render_risk_gauge(score, "ALLOW"), unsafe_allow_html=True)

        # Show low-risk signals plainly as specified
        st.markdown('<div style="font-size: 12px; font-weight: 700; color: #0B1D33; text-transform: uppercase; margin-bottom: 8px;">Security Validation Signals:</div>', unsafe_allow_html=True)
        for sig in signals:
            st.markdown(f"""
            <div style="font-size: 12px; color: #1E9E6B; background: #E7F8F0; padding: 6px 12px; border-radius: 8px; margin-bottom: 6px; font-weight: 500;">
                ✓ {sig}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        col_pay, col_back = st.columns([1.5, 1])
        with col_pay:
            if st.button(f"Confirm & Pay ₹{amount:,.2f}", type="primary", use_container_width=True):
                success = tx_service.record_completed_transaction(
                    transaction_id=tx_id,
                    recipient=recipient,
                    recipient_id=recipient,
                    amount=amount,
                    prediction_result=result
                )
                if success:
                    st.session_state.payment_step = "success"
                    st.rerun()
                else:
                    st.error("Insufficient balance to complete payment.")

        with col_back:
            if st.button("Cancel", use_container_width=True):
                st.session_state.payment_step = "form"
                st.rerun()

# =========================================================================
# 5. SUCCESS SCREEN
# =========================================================================
def _render_success_screen(user: dict, balance: float):
    draft = st.session_state.get("payment_draft", {})
    tx_id = st.session_state.get("current_tx_id", "N/A")
    amount = draft.get("amount", 0.0)
    recipient = draft.get("recipient", "")

    st.markdown("""
    <div style="margin-bottom: 10px;">
        <h1 style="font-size: 20px; font-weight: 700; color: #0B1D33; margin: 0 0 2px 0;">Transfer Status</h1>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 4px 0;">
            <div class="checkmark-circle">
                <svg class="checkmark-icon" viewBox="0 0 24 24">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            </div>
            <div style="font-size: 18px; font-weight: 700; color: #0B1D33; margin-bottom: 2px;">
                Transfer Successful
            </div>
            <div class="money-figure" style="font-size: 26px; font-weight: 700; color: #0B1D33; margin: 4px 0;">
                ₹ {amount:,.2f}
            </div>
            <div style="font-size: 12px; color: #6B7280;">
                Sent to <strong style="color: #0B1D33;">{recipient}</strong>
            </div>
        </div>

        <div style="background: #F7F8FA; border: 1px solid #EDEFF3; border-radius: 10px; padding: 10px 14px; margin: 10px 0 12px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 2px 0;">
                <span style="color: #6B7280;">Transaction ID</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-weight: 600; color: #0B1D33;">{tx_id}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 2px 0;">
                <span style="color: #6B7280;">Updated Balance</span>
                <span style="font-weight: 600; color: #0B1D33;">₹ {balance:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 12px; padding: 2px 0;">
                <span style="color: #6B7280;">Security Verification</span>
                <span style="font-weight: 600; color: #1E9E6B;">✓ Verified by PayGuard AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_new, col_home = st.columns([1, 1])
        with col_new:
            if st.button("Make Another Transfer", type="primary", use_container_width=True):
                st.session_state.pop("payment_draft", None)
                st.session_state.pop("security_result", None)
                st.session_state.pop("current_tx_id", None)
                st.session_state.payment_step = "form"
                st.rerun()

        with col_home:
            if st.button("Back to Home Dashboard", use_container_width=True):
                st.session_state.pop("payment_draft", None)
                st.session_state.pop("security_result", None)
                st.session_state.pop("current_tx_id", None)
                st.session_state.current_screen = "home"
                st.session_state.payment_step = "form"
                st.rerun()
