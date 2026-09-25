"""
PayGuard AI - Authentication Screen Component (Sign In & Registration).
Provides secure dual-mode sign-in and user registration with database persistence.
"""

import os
import re
import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.data.mock_data import DEMO_USERS

def render_login():
    """Renders the client-facing Login and Registration screen."""
    # Ensure auth_mode default
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Navigation link back to project overview
    col_back, _ = st.columns([1, 2])
    with col_back:
        if st.button("← Back to Project Overview", key="btn_back_to_intro", use_container_width=False):
            st.session_state.intro_viewed = False
            st.rerun()

    st.markdown("""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 24px;">🛡️</span>
            <span style="font-size: 24px; font-weight: 800; color: #0B1D33; letter-spacing: -0.03em;">PayGuard</span>
        </div>
        <div style="font-size: 13px; color: #475569; font-weight: 600;">
            Secure payments &bull; Intelligent protection &bull; Instant Ledger
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Card Container with Split Grid
    auth_card = st.container(border=True)
    with auth_card:
        col_img, col_form = st.columns([1.05, 1.25], gap="large")

        # LEFT COLUMN: Visual Brand Illustration & Features
        with col_img:
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            img_path = os.path.join(assets_dir, "login_image.jpeg")
            if not os.path.exists(img_path):
                img_path = os.path.join(assets_dir, "payment_security.jpg")

            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

            st.markdown("""
            <div style="background: #F7F8FA; border: 1px solid #EDEFF3; border-radius: 12px; padding: 14px 16px; margin-top: 14px;">
                <div style="font-size: 13px; font-weight: 700; color: #0B1D33; margin-bottom: 6px;">
                    🔒 Military-Grade Payment Security
                </div>
                <div style="font-size: 11px; color: #6B7280; line-height: 1.5;">
                    Every transaction is protected by 256-bit encryption and evaluated against real-time behavioral models in &lt; 50ms.
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px; font-size: 11px; font-weight: 600; color: #2F5FDE;">
                    <span>✓ ResNeXt-GRU</span>
                    <span>&bull;</span>
                    <span>✓ Double-Entry Check</span>
                    <span>&bull;</span>
                    <span>✓ Zero Paperwork</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # RIGHT COLUMN: Dual Tab Auth Form (Sign In / Register)
        with col_form:
            # Segmented Switcher Header
            c_tab_login, c_tab_reg = st.columns(2)
            is_login_mode = st.session_state.auth_mode == "login"

            with c_tab_login:
                if st.button(
                    "🔑 Sign In",
                    type="primary" if is_login_mode else "secondary",
                    use_container_width=True,
                    key="tab_btn_login"
                ):
                    st.session_state.auth_mode = "login"
                    st.session_state.login_error = None
                    st.session_state.reg_error = None
                    st.rerun()

            with c_tab_reg:
                if st.button(
                    "📝 Create Account",
                    type="primary" if not is_login_mode else "secondary",
                    use_container_width=True,
                    key="tab_btn_reg"
                ):
                    st.session_state.auth_mode = "register"
                    st.session_state.login_error = None
                    st.session_state.reg_error = None
                    st.rerun()

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # =========================================================================
            # A. SIGN IN MODE
            # =========================================================================
            if is_login_mode:
                st.markdown("""
                <div style="margin-bottom: 14px;">
                    <h2 style="font-size: 20px; font-weight: 700; color: #0B1D33; margin: 0 0 2px 0;">Sign In</h2>
                    <div style="font-size: 12px; color: #6B7280;">Enter your registered mobile number or email and 4-digit PIN to access your account.</div>
                </div>
                """, unsafe_allow_html=True)

                default_login_id = st.session_state.get("prefill_mobile", "9876543210")
                default_pin = st.session_state.get("prefill_pin", "1234")

                login_identifier = st.text_input(
                    "Mobile Number or Registered Email",
                    value=default_login_id,
                    placeholder="e.g. 9876543210 or user@example.com",
                    key="input_login_id"
                )

                login_pin = st.text_input(
                    "Security PIN",
                    value=default_pin,
                    type="password",
                    max_chars=6,
                    placeholder="Enter 4-digit PIN",
                    key="input_login_pin"
                )

                col_rem, col_forgot = st.columns([1, 1])
                with col_rem:
                    st.checkbox("Remember me", value=True, key="chk_remember")
                with col_forgot:
                    st.markdown(
                        '<div style="text-align: right; font-size: 12px; color: #2F5FDE; cursor: pointer; padding-top: 4px;" title="PIN resets require verification in sandbox">Forgot PIN?</div>',
                        unsafe_allow_html=True
                    )

                # Error State Display
                if "login_error" in st.session_state and st.session_state.login_error:
                    st.markdown(f"""
                    <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600; margin-bottom: 12px;">
                        ⚠️ {st.session_state.login_error}
                    </div>
                    """, unsafe_allow_html=True)

                # Success notification (e.g. if redirected from registration)
                if "login_success_msg" in st.session_state and st.session_state.login_success_msg:
                    st.markdown(f"""
                    <div style="background: #E7F8F0; border: 1px solid #1E9E6B; color: #1E9E6B; border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600; margin-bottom: 12px;">
                        ✓ {st.session_state.login_success_msg}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.login_success_msg = None

                if st.button("Sign In to Account →", type="primary", use_container_width=True, key="btn_submit_signin"):
                    success, err_msg = AuthService.login(login_identifier, login_pin)
                    if success:
                        st.session_state.login_error = None
                        st.rerun()
                    else:
                        st.session_state.login_error = err_msg
                        st.rerun()

                # Toggle to Register
                st.markdown("""
                <div style="text-align: center; margin: 12px 0 16px 0; font-size: 12px; color: #6B7280;">
                    New to PayGuard?
                </div>
                """, unsafe_allow_html=True)

                if st.button("✨ Don't have an account? Register Now", use_container_width=True, key="btn_goto_register"):
                    st.session_state.auth_mode = "register"
                    st.session_state.login_error = None
                    st.session_state.reg_error = None
                    st.rerun()

                st.markdown("<div style='margin: 16px 0; border-top: 1px solid #EDEFF3;'></div>", unsafe_allow_html=True)

                # Demo Accounts Fast Sign-In for Reviewers
                st.markdown('<div style="font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 8px;">Demo Fast Access (Reviewers):</div>', unsafe_allow_html=True)
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if st.button("Rahul Kumar (9876543210)", use_container_width=True, key="demo_btn_rahul"):
                        st.session_state.prefill_mobile = "9876543210"
                        st.session_state.prefill_pin = "1234"
                        AuthService.login("9876543210", "1234")
                        st.rerun()
                with col_d2:
                    if st.button("Ananya Sharma (9123456780)", use_container_width=True, key="demo_btn_ananya"):
                        st.session_state.prefill_mobile = "9123456780"
                        st.session_state.prefill_pin = "5678"
                        AuthService.login("9123456780", "5678")
                        st.rerun()

            # =========================================================================
            # B. REGISTRATION MODE
            # =========================================================================
            else:
                st.markdown("""
                <div style="margin-bottom: 14px;">
                    <h2 style="font-size: 20px; font-weight: 700; color: #0B1D33; margin: 0 0 2px 0;">Create Account</h2>
                    <div style="font-size: 12px; color: #6B7280;">Fill in your details to open your AI-protected digital banking wallet.</div>
                </div>
                """, unsafe_allow_html=True)

                reg_name = st.text_input(
                    "Full Name",
                    placeholder="e.g. Priya Sharma",
                    key="reg_name_input"
                )

                c_reg_m, c_reg_e = st.columns([1, 1])
                with c_reg_m:
                    reg_mobile = st.text_input(
                        "Mobile Number (10 Digits)",
                        placeholder="e.g. 9876501234",
                        max_chars=10,
                        key="reg_mobile_input"
                    )
                with c_reg_e:
                    reg_email = st.text_input(
                        "Email Address",
                        placeholder="e.g. priya@example.com",
                        key="reg_email_input"
                    )

                c_pin1, c_pin2 = st.columns(2)
                with c_pin1:
                    reg_pin = st.text_input(
                        "4-Digit Security PIN",
                        type="password",
                        max_chars=4,
                        placeholder="••••",
                        key="reg_pin_input"
                    )
                with c_pin2:
                    reg_pin_confirm = st.text_input(
                        "Confirm Security PIN",
                        type="password",
                        max_chars=4,
                        placeholder="••••",
                        key="reg_pin_confirm_input"
                    )

                reg_balance = st.number_input(
                    "Initial Wallet Balance Deposit (₹)",
                    min_value=1000.0,
                    max_value=500000.0,
                    value=50000.0,
                    step=5000.0,
                    format="%.2f",
                    key="reg_balance_input"
                )

                # Dynamic Preview Box for User Info
                computed_upi = f"{reg_name.strip().lower().replace(' ', '.')}@payguard" if reg_name.strip() else "yourname@payguard"
                st.markdown(f"""
                <div style="background: #EEF3FF; border: 1px solid #D0E1FD; border-radius: 8px; padding: 10px 14px; margin: 10px 0 14px 0; font-size: 11px;">
                    <div style="font-weight: 700; color: #2F5FDE; margin-bottom: 2px;">⚡ Live Account Setup Preview:</div>
                    <div style="color: #475569;">
                        &bull; Virtual UPI Address: <code style="color: #2F5FDE; font-weight: 600;">{computed_upi}</code><br>
                        &bull; Initial Wallet Balance: <strong>₹{reg_balance:,.2f}</strong><br>
                        &bull; Data Persistence: Stored securely in <strong>payguard_bank.db</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Registration Error Display
                if "reg_error" in st.session_state and st.session_state.reg_error:
                    st.markdown(f"""
                    <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 10px 14px; font-size: 12px; font-weight: 600; margin-bottom: 12px;">
                        ⚠️ {st.session_state.reg_error}
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("Complete Registration & Open Account →", type="primary", use_container_width=True, key="btn_submit_register"):
                    # Form validation
                    if not reg_name.strip():
                        st.session_state.reg_error = "Please enter your full name."
                        st.rerun()
                    elif not reg_mobile.strip().isdigit() or len(reg_mobile.strip()) != 10:
                        st.session_state.reg_error = "Mobile number must be exactly 10 digits."
                        st.rerun()
                    elif "@" not in reg_email or "." not in reg_email:
                        st.session_state.reg_error = "Please enter a valid email address."
                        st.rerun()
                    elif not reg_pin.strip().isdigit() or len(reg_pin.strip()) != 4:
                        st.session_state.reg_error = "Security PIN must be exactly 4 digits."
                        st.rerun()
                    elif reg_pin.strip() != reg_pin_confirm.strip():
                        st.session_state.reg_error = "Security PIN and Confirmation PIN do not match."
                        st.rerun()
                    else:
                        success, err_msg, new_user = AuthService.register(
                            name=reg_name.strip(),
                            mobile=reg_mobile.strip(),
                            email=reg_email.strip(),
                            pin=reg_pin.strip(),
                            initial_balance=float(reg_balance)
                        )

                        if success and new_user:
                            # Automatically authenticate the new user into their freshly minted account
                            st.session_state.authenticated_user = new_user
                            if "wallet_balances" not in st.session_state:
                                st.session_state.wallet_balances = {}
                            st.session_state.wallet_balances[new_user["user_id"]] = float(new_user["available_balance"])
                            st.session_state.current_screen = "home"
                            st.session_state.login_error = None
                            st.session_state.reg_error = None
                            st.rerun()
                        else:
                            st.session_state.reg_error = err_msg
                            st.rerun()

                # Toggle back to Sign In
                st.markdown("""
                <div style="text-align: center; margin: 12px 0 6px 0; font-size: 12px; color: #6B7280;">
                    Already have an account?
                </div>
                """, unsafe_allow_html=True)

                if st.button("← Already Registered? Sign In Here", use_container_width=True, key="btn_goto_login"):
                    st.session_state.auth_mode = "login"
                    st.session_state.login_error = None
                    st.session_state.reg_error = None
                    st.rerun()

    # Small, unobtrusive sandbox footer
    st.markdown("""
    <div style="text-align: center; margin-top: 24px; font-size: 11px; font-weight: 600; color: #6B7280; letter-spacing: 0.05em;">
        SANDBOX • NO REAL MONEY &bull; SQLITE BACKED
    </div>
    """, unsafe_allow_html=True)
