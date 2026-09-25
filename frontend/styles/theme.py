"""
PayGuard AI - Design System Tokens & Injected CSS.
Single source of truth for color palette, typography, elevation, and component styles.
"""

import streamlit as st

# Design Tokens (Constants)
NAVY_900 = "#0B1D33"
BLUE_600 = "#2F5FDE"
BLUE_50 = "#EEF3FF"
SUCCESS_600 = "#1E9E6B"
SUCCESS_50 = "#E7F8F0"
AMBER_600 = "#B7791F"
AMBER_50 = "#FFF6E5"
DANGER_600 = "#C0392B"
DANGER_50 = "#FDECEA"
NEUTRAL_50 = "#F7F8FA"
NEUTRAL_100 = "#EDEFF3"
NEUTRAL_500 = "#6B7280"
NEUTRAL_900 = "#111827"

CARD_RADIUS = "16px"
PILL_RADIUS = "999px"
CARD_SHADOW = "0 8px 24px rgba(15, 23, 42, 0.06)"

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --navy-900: {NAVY_900};
    --blue-600: {BLUE_600};
    --blue-50: {BLUE_50};
    --success-600: {SUCCESS_600};
    --success-50: {SUCCESS_50};
    --amber-600: {AMBER_600};
    --amber-50: {AMBER_50};
    --danger-600: {DANGER_600};
    --danger-50: {DANGER_50};
    --neutral-50: {NEUTRAL_50};
    --neutral-100: {NEUTRAL_100};
    --neutral-500: {NEUTRAL_500};
    --neutral-900: {NEUTRAL_900};
    --radius-card: {CARD_RADIUS};
    --radius-pill: {PILL_RADIUS};
    --shadow-soft: {CARD_SHADOW};
}}

/* Base Styles */
html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--neutral-900);
    background-color: var(--neutral-50) !important;
    -webkit-font-smoothing: antialiased;
}}

/* Remove default Streamlit top header clutter */
header[data-testid="stHeader"] {{
    background-color: transparent !important;
    z-index: 10 !important;
}}

/* Smooth Fade Transition for screen changes */
[data-testid="stMainBlockContainer"] {{
    animation: fadeInPage 0.25s ease-out;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1080px !important;
}}

@keyframes fadeInPage {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Typography System */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    color: var(--navy-900);
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}}

.intro-hero h1, .intro-hero h2, .intro-hero h3, .intro-title {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
}}

/* Money Figures Typography */
.money-figure {{
    font-family: 'Inter', -apple-system, sans-serif;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--navy-900);
}}

/* Buttons Styling */
button[kind="primary"], .stButton > button[kind="primary"] {{
    background-color: var(--blue-600) !important;
    color: #FFFFFF !important;
    border-radius: var(--radius-pill) !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(47, 95, 222, 0.2) !important;
    transition: all 0.15s ease !important;
}}

button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {{
    background-color: #244ec2 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(47, 95, 222, 0.28) !important;
}}

button[kind="secondary"], .stButton > button[kind="secondary"] {{
    background-color: #FFFFFF !important;
    color: var(--neutral-900) !important;
    border-radius: var(--radius-pill) !important;
    border: 1px solid var(--neutral-100) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
    transition: all 0.15s ease !important;
}}

button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {{
    background-color: var(--neutral-50) !important;
    border-color: #CBD5E1 !important;
}}

/* Inputs Styling */
input, div[data-baseweb="input"] {{
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    border-color: var(--neutral-100) !important;
}}

input:focus, div[data-baseweb="input"]:focus-within {{
    border-color: var(--blue-600) !important;
    box-shadow: 0 0 0 3px rgba(47, 95, 222, 0.15) !important;
}}

/* Custom Section Card Container */
.pg-card {{
    background: #FFFFFF;
    border-radius: var(--radius-card);
    border: 1px solid var(--neutral-100);
    box-shadow: var(--shadow-soft);
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}

/* Status Pills */
.status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: var(--radius-pill);
    font-size: 12px;
    font-weight: 600;
    line-height: 1.4;
}}

.status-pill-active {{
    background: var(--success-50);
    color: var(--success-600);
}}

.status-pill-connected {{
    background: var(--success-50);
    color: var(--success-600);
}}

.status-pill-offline {{
    background: var(--danger-50);
    color: var(--danger-600);
}}

.status-pill-verify {{
    background: var(--amber-50);
    color: var(--amber-600);
}}

.status-pill-neutral {{
    background: var(--neutral-100);
    color: var(--neutral-500);
}}

/* Signal Chips */
.signal-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--neutral-50);
    border: 1px solid var(--neutral-100);
    border-radius: 8px;
    font-size: 12px;
    color: var(--neutral-900);
    font-weight: 500;
}}

/* Transaction Row */
.tx-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid var(--neutral-100);
}}

.tx-row:last-child {{
    border-bottom: none;
}}

/* Checkmark draw-in animation for Success screen */
@keyframes checkmarkDraw {{
    0% {{
        stroke-dashoffset: 48;
    }}
    100% {{
        stroke-dashoffset: 0;
    }}
}}

.checkmark-circle {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--success-50);
    color: var(--success-600);
    margin-bottom: 16px;
}}

.checkmark-icon {{
    width: 32px;
    height: 32px;
    stroke: var(--success-600);
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: checkmarkDraw 0.4s ease-in-out forwards 0.1s;
}}

/* Decision Morph Circle */
.decision-circle {{
    width: 72px;
    height: 72px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px auto;
    transition: background-color 0.3s ease;
}}

.decision-circle.allow {{
    background: var(--success-50);
    color: var(--success-600);
}}

.decision-circle.verify {{
    background: var(--amber-50);
    color: var(--amber-600);
}}

.decision-circle.review {{
    background: var(--danger-50);
    color: var(--danger-600);
}}

.decision-circle.reconciliation {{
    background: var(--neutral-100);
    color: var(--neutral-500);
}}

/* Count-up animation helper */
@keyframes countUpReveal {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.count-up-text {{
    display: inline-block;
    animation: countUpReveal 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

/* Intro Webpage Styling & Animations */
@keyframes introFadeIn {{
    0% {{ opacity: 0; transform: translateY(12px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

.intro-container {{
    animation: introFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.intro-hero {{
    background: linear-gradient(135deg, #0B1D33 0%, #173259 100%);
    border-radius: 24px;
    padding: 48px 40px;
    color: #FFFFFF;
    box-shadow: 0 16px 40px rgba(11, 29, 51, 0.12);
    position: relative;
    overflow: hidden;
    margin-bottom: 28px;
}}

.intro-hero::after {{
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 380px;
    height: 380px;
    background: radial-gradient(circle, rgba(47, 95, 222, 0.25) 0%, transparent 70%);
    pointer-events: none;
}}

.intro-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: var(--radius-pill);
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.18);
    font-size: 11px;
    font-weight: 700;
    color: #90E0EF;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 18px;
}}

.pulse-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ADE80;
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7);
    animation: pulseGlow 2s infinite;
}}

@keyframes pulseGlow {{
    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7); }}
    70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(74, 222, 128, 0); }}
    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(74, 222, 128, 0); }}
}}

.intro-feature-card {{
    background: #FFFFFF;
    border: 1px solid var(--neutral-100);
    border-radius: var(--radius-card);
    padding: 24px;
    height: 100%;
    box-shadow: var(--shadow-soft);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.intro-feature-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.09);
    border-color: #CBD5E1;
}}

.intro-stat-box {{
    background: #F7F8FA;
    border: 1px solid #EDEFF3;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}}
</style>
"""

def inject_theme():
    """Injects design tokens and CSS into current Streamlit session."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def render_status_pill(status: str, label: str = None) -> str:
    """Renders an inline status pill HTML component."""
    status_lower = status.lower()
    text = label or status
    pill_class = "status-pill-neutral"
    dot_color = NEUTRAL_500
    
    if "active" in status_lower or "connected" in status_lower or "allow" in status_lower or "completed" in status_lower:
        pill_class = "status-pill-active"
        dot_color = SUCCESS_600
    elif "offline" in status_lower or "review" in status_lower or "failed" in status_lower or "blocked" in status_lower:
        pill_class = "status-pill-offline"
        dot_color = DANGER_600
    elif "verify" in status_lower or "reconciliation" in status_lower or "pending" in status_lower:
        pill_class = "status-pill-verify"
        dot_color = AMBER_600

    return f'''<span class="status-pill {pill_class}">
        <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:{dot_color};"></span>
        <span>{text}</span>
    </span>'''

def render_risk_gauge(score: int, decision: str) -> str:
    """Renders a clean radial risk gauge (0-100) colored by decision band."""
    score = max(0, min(100, int(score)))
    if decision == "ALLOW":
        color = SUCCESS_600
        bg_track = SUCCESS_50
        status_text = "Low Risk • Passed"
    elif decision == "VERIFY":
        color = AMBER_600
        bg_track = AMBER_50
        status_text = "Elevated Risk • Verification Step"
    elif decision == "REVIEW":
        color = DANGER_600
        bg_track = DANGER_50
        status_text = "High Risk • Payment Blocked"
    else:
        color = NEUTRAL_500
        bg_track = NEUTRAL_100
        status_text = "Reconciliation Required"

    # SVG circle calculation (radius = 38, circumference = 238.76)
    radius = 38
    circumference = 2 * 3.14159 * radius
    dash_offset = circumference - (score / 100.0) * circumference

    return f'''
    <div style="text-align: center; margin: 16px 0;">
        <div style="position: relative; width: 100px; height: 100px; margin: 0 auto;">
            <svg width="100" height="100" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="{radius}" fill="none" stroke="{bg_track}" stroke-width="8"/>
                <circle cx="50" cy="50" r="{radius}" fill="none" stroke="{color}" stroke-width="8"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dash_offset}"
                    stroke-linecap="round" style="transition: stroke-dashoffset 0.6s ease;"/>
            </svg>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-size: 22px; font-weight: 700; color: {NAVY_900}; font-family: 'Inter', sans-serif;">{score}</span>
                <span style="font-size: 10px; color: {NEUTRAL_500}; font-weight: 600; text-transform: uppercase;">Score</span>
            </div>
        </div>
        <div style="font-size: 12px; font-weight: 600; color: {color}; margin-top: 8px;">{status_text}</div>
    </div>
    '''

def render_money_text(amount: float, currency: str = "₹", size: str = "28px", label: str = None) -> str:
    """Renders formatted money text with clean typography."""
    formatted = f"{amount:,.2f}"
    sub = f'<div style="font-size: 12px; color: {NEUTRAL_500}; margin-top: 4px;">{label}</div>' if label else ""
    return f'''
    <div>
        <div class="money-figure count-up-text" style="font-size: {size}; line-height: 1.1;">
            <span style="font-size: 0.75em; opacity: 0.85; margin-right: 2px;">{currency}</span>{formatted}
        </div>
        {sub}
    </div>
    '''

def render_signal_chip(icon: str, label: str) -> str:
    """Renders a single security signal chip."""
    return f'''
    <span class="signal-chip">
        <span>{icon}</span>
        <span>{label}</span>
    </span>
    '''
