"""
PayGuard AI - Authentication Screen Component (Log In & Create Account).
Features Email + Confirmation Code + Password + Confirm Password + UPI PIN workflow.
Optimized for 100% desktop site viewports with zero vertical scrolling required.
"""

import os
import re
import streamlit as st
from frontend.services.auth_service import AuthService
from frontend.services.clerk_service import ClerkAuthService
from frontend.data.mock_data import DEMO_USERS

def render_login():
    """Renders the streamlined Log In and Create Account screen fitted for 100% desktop viewports."""
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Compact Header Bar (Back button + Logo inline)
    col_nav_left, col_nav_right = st.columns([1, 2])
    with col_nav_left:
        if st.button("← Back to Project Overview", key="btn_back_to_intro", use_container_width=False):
            st.session_state.intro_viewed = False
            st.rerun()

    with col_nav_right:
        st.markdown("""
        <div style="text-align: right; padding-right: 4px;">
            <span style="font-size: 18px; font-weight: 800; color: #001D39; letter-spacing: -0.02em;">🛡️ PayGuard</span>
            <span style="font-size: 11px; color: #49769F; font-weight: 600; margin-left: 8px;">• Intelligent Protection</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    # Main Card Container with Compact Split Grid
    auth_card = st.container(border=True)
    with auth_card:
        col_img, col_form = st.columns([1.0, 1.3], gap="large")

        # LEFT COLUMN: Visual Brand Illustration & Features
        with col_img:
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            img_path = os.path.join(assets_dir, "login_image.jpeg")
            if not os.path.exists(img_path):
                img_path = os.path.join(assets_dir, "payment_security.jpg")

            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

            st.markdown("""
            <div style="background: #F0F6FA; border: 1px solid #BDD8E9; border-radius: 10px; padding: 10px 14px; margin-top: 8px;">
                <div style="font-size: 12px; font-weight: 700; color: #001D39; margin-bottom: 3px;">
                    🔒 Military-Grade Payment Protection
                </div>
                <div style="font-size: 11px; color: #49769F; line-height: 1.4;">
                    Protected by 256-bit encryption & evaluated against real-time PyTorch ResNeXt-GRU models in &lt; 50ms.
                </div>
                <div style="display: flex; gap: 8px; margin-top: 6px; font-size: 10.5px; font-weight: 700; color: #0A4174;">
                    <span>✓ ResNeXt-GRU</span>
                    <span>&bull;</span>
                    <span>✓ Double-Entry Check</span>
                    <span>&bull;</span>
                    <span>✓ Email Verified</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # RIGHT COLUMN: Dual Tab Auth Form (Log In / Create Account)
        with col_form:
            c_tab_login, c_tab_reg = st.columns(2)
            is_login_mode = st.session_state.auth_mode == "login"

            with c_tab_login:
                if st.button(
                    "🔑 Log In",
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

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

            # =========================================================================
            # A. LOG IN MODE
            # =========================================================================
            if is_login_mode:
                st.markdown("""
                <div style="margin-bottom: 8px;">
                    <h2 style="font-size: 18px; font-weight: 800; color: #001D39; margin: 0 0 2px 0;">Log In</h2>
                    <div style="font-size: 11.5px; color: #49769F;">Enter your registered Mail ID and Password to sign in to your account.</div>
                </div>
                """, unsafe_allow_html=True)

                default_login_id = st.session_state.get("prefill_email", "")
                default_password = st.session_state.get("prefill_password", "")

                login_identifier = st.text_input(
                    "Mail ID",
                    value=default_login_id,
                    placeholder="e.g. user@example.com",
                    key="input_login_id"
                )

                login_password = st.text_input(
                    "Password",
                    value=default_password,
                    type="password",
                    max_chars=32,
                    placeholder="Enter Password",
                    key="input_login_pin"
                )

                col_rem, col_forgot = st.columns([1, 1])
                with col_rem:
                    st.checkbox("Remember me", value=True, key="chk_remember")
                with col_forgot:
                    st.markdown(
                        '<div style="text-align: right; font-size: 11px; color: #0A4174; cursor: pointer; padding-top: 2px;" title="Password resets require verification in sandbox">Forgot Password?</div>',
                        unsafe_allow_html=True
                    )

                # Error State Display
                if "login_error" in st.session_state and st.session_state.login_error:
                    st.markdown(f"""
                    <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 6px 10px; font-size: 11px; font-weight: 600; margin-bottom: 8px;">
                        ⚠️ {st.session_state.login_error}
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("Log In to Account →", type="primary", use_container_width=True, key="btn_submit_signin"):
                    success, err_msg = AuthService.login(login_identifier, login_password)
                    if success:
                        st.session_state.login_error = None
                        st.rerun()
                    else:
                        st.session_state.login_error = err_msg
                        st.rerun()

            # =========================================================================
            # B. CREATE ACCOUNT MODE (Multi-Step Page Transition: Step 1 -> Step 2)
            # =========================================================================
            else:
                reg_step = st.session_state.get("reg_step", 1)
                is_verified = st.session_state.get("email_verified", False) and st.session_state.get("verified_email") is not None

                # ---------------------------------------------------------------------
                # STEP 2 (NEXT PAGE): PASSWORD & 4-DIGIT UPI PIN SETUP
                # ---------------------------------------------------------------------
                if reg_step == 2 and is_verified:
                    verified_m = st.session_state.get("verified_email", "")
                    verified_n = st.session_state.get("verified_name", "User")
                    verified_mob = st.session_state.get("verified_mobile", "")

                    st.markdown(f"""
                    <div style="margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="font-size: 18px; font-weight: 800; color: #001D39; margin: 0;">Step 2: Security Setup</h2>
                            <span style="background: #10B981; color: #FFFFFF; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 999px;">
                                ✅ Mail ID Verified
                            </span>
                        </div>
                        <div style="font-size: 11.5px; color: #49769F; margin-top: 2px;">Set your login Password and 4-Digit UPI PIN for transactions.</div>
                    </div>
                    <div style="background: #F4F0FF; border: 1px solid #6C47FF; color: #3C1E99; border-radius: 8px; padding: 8px 12px; font-size: 11.5px; font-weight: 700; margin-bottom: 12px;">
                        👤 <b>{verified_n}</b> &bull; 📱 <b>+91 {verified_mob}</b> &bull; ✉️ <u>{verified_m}</u>
                    </div>
                    """, unsafe_allow_html=True)

                    c_p1, c_p2 = st.columns(2)
                    with c_p1:
                        reg_pass = st.text_input(
                            "Password (Min 8 Chars, Letter + Number)",
                            type="password",
                            placeholder="Enter password",
                            key="reg_pass_input"
                        )
                    with c_p2:
                        reg_pass_confirm = st.text_input(
                            "Confirm Password",
                            type="password",
                            placeholder="Re-enter password",
                            key="reg_pass_confirm_input"
                        )

                    reg_pin = st.text_input(
                        "Set 4-Digit UPI PIN (For Money Transfers)",
                        type="password",
                        max_chars=4,
                        placeholder="e.g. 1234",
                        key="reg_pin_input"
                    )

                    # Registration Error Display
                    if "reg_error" in st.session_state and st.session_state.reg_error:
                        st.markdown(f"""
                        <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 6px 10px; font-size: 11px; font-weight: 600; margin-bottom: 8px;">
                            ⚠️ {st.session_state.reg_error}
                        </div>
                        """, unsafe_allow_html=True)

                    c_b1, c_b2 = st.columns([1, 2])
                    with c_b1:
                        if st.button("← Back", use_container_width=True, key="btn_reg_back_step1"):
                            st.session_state.reg_step = 1
                            st.rerun()

                    with c_b2:
                        if st.button("🚀 Complete Account & Log In →", type="primary", use_container_width=True, key="btn_submit_register"):
                            clean_p = reg_pass.strip()
                            clean_p2 = reg_pass_confirm.strip()
                            clean_pin = reg_pin.strip()

                            if len(clean_p) < 8 or not any(c.isalpha() for c in clean_p) or not any(c.isdigit() or not c.isalnum() for c in clean_p):
                                st.session_state.reg_error = "Password must be at least 8 characters long with at least 1 letter and 1 number/special character."
                                st.rerun()
                            elif clean_p != clean_p2:
                                st.session_state.reg_error = "Password and Confirm Password do not match."
                                st.rerun()
                            elif not clean_pin.isdigit() or len(clean_pin) != 4:
                                st.session_state.reg_error = "UPI PIN must be exactly 4 digits."
                                st.rerun()
                            else:
                                success, err_msg, new_user = AuthService.register(
                                    name=verified_n,
                                    mobile=verified_mob,
                                    email=verified_m,
                                    pin=clean_pin,
                                    password=clean_p,
                                    initial_balance=50000.0
                                )

                                if success and new_user:
                                    st.session_state.authenticated_user = new_user
                                    if "wallet_balances" not in st.session_state:
                                        st.session_state.wallet_balances = {}
                                    st.session_state.wallet_balances[new_user["user_id"]] = float(new_user["available_balance"])
                                    st.session_state.current_screen = "home"
                                    st.session_state.login_error = None
                                    st.session_state.reg_error = None
                                    st.session_state.code_sent_msg = None
                                    st.session_state.code_sent_info = None
                                    st.session_state.email_verified = False
                                    st.session_state.verified_email = None
                                    st.session_state.reg_step = 1
                                    st.rerun()
                                else:
                                    st.session_state.reg_error = err_msg
                                    st.rerun()

                # ---------------------------------------------------------------------
                # STEP 1 (FIRST PAGE): FULL NAME, MOBILE, MAIL ID & CLERK VERIFICATION
                # ---------------------------------------------------------------------
                else:
                    st.markdown("""
                    <div style="margin-bottom: 6px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="font-size: 18px; font-weight: 800; color: #001D39; margin: 0;">Create Account</h2>
                            <span style="background: #6C47FF; color: #FFFFFF; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 999px;">
                                🔒 Clerk Auth Engine (clerk.com)
                            </span>
                        </div>
                        <div style="font-size: 11.5px; color: #49769F; margin-top: 2px;">Step 1: Enter details & verify Mail ID &bull; Step 2: Set Password on next page.</div>
                    </div>
                    """, unsafe_allow_html=True)

                    c_n1, c_n2 = st.columns(2)
                    with c_n1:
                        reg_name_pre = st.text_input(
                            "Full Name",
                            value=st.session_state.get("verified_name", ""),
                            placeholder="e.g. Rahul Kumar",
                            key="reg_name_input"
                        )
                    with c_n2:
                        reg_mobile_pre = st.text_input(
                            "Mobile Number (10 Digits)",
                            value=st.session_state.get("verified_mobile", ""),
                            placeholder="e.g. 9876543210",
                            max_chars=13,
                            key="reg_mobile_input"
                        )

                    c_m1, c_m2 = st.columns([1.5, 1])
                    with c_m1:
                        reg_email = st.text_input(
                            "Mail ID",
                            value=st.session_state.get("verified_email", ""),
                            placeholder="e.g. user@example.com",
                            key="reg_email_input"
                        )
                    with c_m2:
                        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                        if st.button("✉️ Send Clerk Code", use_container_width=True, key="btn_send_email_code"):
                            ok_code, msg_code, gen_code = ClerkAuthService.send_email_code(reg_email)
                            st.session_state.email_verified = False
                            st.session_state.verified_email = None
                            if ok_code:
                                st.session_state.code_sent_msg = msg_code
                                st.session_state.reg_error = None
                                st.rerun()
                            else:
                                st.session_state.reg_error = msg_code
                                st.rerun()

                    # Display Confirmation Code Sent Notification
                    clerk_info = st.session_state.get("clerk_sent_info")
                    info = st.session_state.get("code_sent_info")
                    target_info = clerk_info or info

                    if target_info and target_info.get("email"):
                        st.markdown(f"""
                        <div style="background: #F4F0FF; border: 1px solid #B89CFF; color: #3C1E99; border-radius: 8px; padding: 10px 14px; margin-bottom: 10px;">
                            <div style="font-size: 12.5px; font-weight: 700; color: #1E0A52; margin-bottom: 4px;">
                                📬 Verification Code Sent to <u>{target_info['email']}</u>
                            </div>
                            <div style="font-size: 11px; color: #5B38D8; line-height: 1.4;">
                                Please check your email inbox at <b>{target_info['email']}</b>, copy the 6-digit verification code sent to your Mail ID, and enter it below.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif st.session_state.get("code_sent_msg"):
                        st.markdown(f"""
                        <div style="background: #F4F0FF; border: 1px solid #B89CFF; color: #3C1E99; border-radius: 8px; padding: 8px 12px; font-size: 11px; font-weight: 600; margin-bottom: 8px;">
                            📬 Verification code sent to your Mail ID! Please check your email inbox.
                        </div>
                        """, unsafe_allow_html=True)

                    # CODE ENTRY + VERIFY BUTTON VIA CLERK -> ADVANCES TO STEP 2 (NEXT PAGE)
                    c_vc1, c_vc2 = st.columns([1.5, 1])
                    with c_vc1:
                        reg_code = st.text_input(
                            "6-Digit Verification Code",
                            placeholder="Enter 6-digit code received on your Mail ID",
                            max_chars=6,
                            key="reg_code_input"
                        )
                    with c_vc2:
                        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                        if st.button("✅ Verify & Continue →", use_container_width=True, key="btn_verify_code_now"):
                            clean_name = reg_name_pre.strip()
                            clean_mob = reg_mobile_pre.strip().replace(" ", "").replace("-", "")
                            if len(clean_mob) == 12 and clean_mob.startswith("91"):
                                clean_mob = clean_mob[2:]
                            elif len(clean_mob) == 13 and clean_mob.startswith("+91"):
                                clean_mob = clean_mob[3:]

                            clean_m = reg_email.strip().lower()
                            clean_c = reg_code.strip()

                            if not clean_name or len(clean_name) < 2:
                                st.session_state.reg_error = "Please enter your Full Name (at least 2 characters)."
                                st.rerun()
                            elif not clean_mob.isdigit() or len(clean_mob) != 10:
                                st.session_state.reg_error = "Please enter a valid 10-digit Mobile Number."
                                st.rerun()
                            elif not clean_m or "@" not in clean_m:
                                st.session_state.reg_error = "Please enter your valid Mail ID first."
                                st.session_state.email_verified = False
                                st.rerun()
                            elif not clean_c:
                                st.session_state.reg_error = "Please enter the 6-digit Clerk verification code sent to your Mail ID."
                                st.session_state.email_verified = False
                                st.rerun()
                            else:
                                ok_clerk, msg_clerk = ClerkAuthService.verify_email_code(clean_m, clean_c)
                                if ok_clerk or AuthService.verify_email_confirmation_code(clean_m, clean_c):
                                    st.session_state.email_verified = True
                                    st.session_state.verified_email = clean_m
                                    st.session_state.verified_name = clean_name
                                    st.session_state.verified_mobile = clean_mob
                                    st.session_state.reg_step = 2  # MOVE TO NEXT PAGE!
                                    st.session_state.reg_error = None
                                    st.rerun()
                                else:
                                    st.session_state.email_verified = False
                                    st.session_state.reg_error = f"⚠️ {msg_clerk}"
                                    st.rerun()

                    # Registration Error Display
                    if "reg_error" in st.session_state and st.session_state.reg_error:
                        st.markdown(f"""
                        <div style="background: #FDECEA; border: 1px solid #C0392B; color: #C0392B; border-radius: 8px; padding: 6px 10px; font-size: 11px; font-weight: 600; margin-top: 6px; margin-bottom: 8px;">
                            ⚠️ {st.session_state.reg_error}
                        </div>
                        """, unsafe_allow_html=True)

    # Small sandbox footer
    st.markdown("""
    <div style="text-align: center; margin-top: 10px; font-size: 10.5px; font-weight: 600; color: #49769F; letter-spacing: 0.05em;">
        SANDBOX • NO REAL MONEY &bull; SQLITE BACKED
    </div>
    """, unsafe_allow_html=True)
