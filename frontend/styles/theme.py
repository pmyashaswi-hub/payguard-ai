"""
PayGuard AI - Design System Tokens & Injected CSS.
Integrated with the user-provided Oceanic Blue color palette:
- #001D39 (Deep Oceanic Navy)
- #0A4174 (Royal Ocean Blue)
- #49769F (Slate Steel Blue)
- #4E8EA2 (Ocean Teal Cyan)
- #6EA2B3 (Muted Ice Teal)
- #7BBDE8 (Sky Blue)
- #BDD8E9 (Soft Powder Blue)
"""

import streamlit as st

# Palette Tokens (Extracted from User Palette Image)
COLOR_001D39 = "#001D39"  # Deep Oceanic Navy
COLOR_0A4174 = "#0A4174"  # Royal Ocean Blue
COLOR_49769F = "#49769F"  # Slate Steel Blue
COLOR_4E8EA2 = "#4E8EA2"  # Ocean Teal Cyan
COLOR_6EA2B3 = "#6EA2B3"  # Muted Ice Teal
COLOR_7BBDE8 = "#7BBDE8"  # Sky Blue
COLOR_BDD8E9 = "#BDD8E9"  # Soft Powder Blue

# Semantic Token Mapping
NAVY_900 = COLOR_001D39
BLUE_600 = COLOR_0A4174
BLUE_50 = "#EBF4F9"
SUCCESS_600 = "#1E9E6B"
SUCCESS_50 = "#E7F8F0"
AMBER_600 = "#B7791F"
AMBER_50 = "#FFF6E5"
DANGER_600 = "#C0392B"
DANGER_50 = "#FDECEA"
NEUTRAL_50 = "#F3F7FA"
NEUTRAL_100 = COLOR_BDD8E9
NEUTRAL_500 = COLOR_49769F
NEUTRAL_900 = COLOR_001D39

CARD_RADIUS = "16px"
PILL_RADIUS = "999px"
CARD_SHADOW = "0 8px 24px rgba(0, 29, 57, 0.06)"

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --navy-900: {NAVY_900};
    --blue-600: {BLUE_600};
    --blue-50: {BLUE_50};
    --color-001d39: {COLOR_001D39};
    --color-0a4174: {COLOR_0A4174};
    --color-49769f: {COLOR_49769F};
    --color-4e8ea2: {COLOR_4E8EA2};
    --color-6ea2b3: {COLOR_6EA2B3};
    --color-7bbde8: {COLOR_7BBDE8};
    --color-bdd8e9: {COLOR_BDD8E9};
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

/* Base Page Background with Soft Oceanic Palette Tint */
html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--navy-900);
    background-color: var(--neutral-50) !important;
    background-image: radial-gradient({COLOR_BDD8E9} 0.6px, transparent 0.6px) !important;
    background-size: 16px 16px !important;
    -webkit-font-smoothing: antialiased;
}}

/* Header & Sidebar */
header[data-testid="stHeader"] {{
    background-color: transparent !important;
    z-index: 10 !important;
}}

section[data-testid="stSidebar"] {{
    background: #FFFFFF !important;
    border-right: 1px solid {COLOR_BDD8E9} !important;
    box-shadow: 4px 0 20px rgba(0, 29, 57, 0.04) !important;
}}

/* Page Container Animation & Viewport Spacing */
[data-testid="stMainBlockContainer"] {{
    animation: fadeInPage 0.25s ease-out;
    padding-top: 0.4rem !important;
    padding-bottom: 0.8rem !important;
    max-width: 1040px !important;
}}

@keyframes fadeInPage {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Typography System */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    color: {COLOR_001D39} !important;
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
    font-weight: 700;
    letter-spacing: -0.02em;
    color: {COLOR_001D39};
}}

/* Primary Buttons (Royal Ocean Blue #0A4174) */
button[kind="primary"], .stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {COLOR_0A4174} 0%, {COLOR_001D39} 100%) !important;
    color: #FFFFFF !important;
    border-radius: var(--radius-pill) !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(10, 65, 116, 0.3) !important;
    transition: all 0.15s ease !important;
}}

button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {{
    background: {COLOR_001D39} !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(0, 29, 57, 0.4) !important;
}}

/* Secondary Buttons (White with Slate Steel Blue #6EA2B3 border) */
button[kind="secondary"], .stButton > button[kind="secondary"] {{
    background-color: #FFFFFF !important;
    color: {COLOR_001D39} !important;
    border-radius: var(--radius-pill) !important;
    border: 1.5px solid {COLOR_6EA2B3} !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 2px 6px rgba(0, 29, 57, 0.04) !important;
    transition: all 0.15s ease !important;
}}

button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {{
    background-color: {COLOR_BDD8E9} !important;
    border-color: {COLOR_0A4174} !important;
}}

/* Form Input Styling */
input, div[data-baseweb="input"] {{
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    border-color: {COLOR_BDD8E9} !important;
}}

input:focus, div[data-baseweb="input"]:focus-within {{
    border-color: {COLOR_0A4174} !important;
    box-shadow: 0 0 0 3px rgba(10, 65, 116, 0.15) !important;
}}

/* Custom Section Card Container */
.pg-card {{
    background: #FFFFFF;
    border-radius: var(--radius-card);
    border: 1px solid {COLOR_BDD8E9};
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
    background: {COLOR_BDD8E9};
    color: {COLOR_001D39};
}}

/* Signal Chips */
.signal-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: #F0F6FA;
    border: 1px solid {COLOR_BDD8E9};
    border-radius: 8px;
    font-size: 12px;
    color: {COLOR_001D39};
    font-weight: 600;
}}

/* Transaction Row */
.tx-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid {COLOR_BDD8E9};
}}

.tx-row:last-child {{
    border-bottom: none;
}}

/* Intro Hero Banner (Gradated Deep Navy to Royal Blue to Ocean Teal) */
.intro-hero {{
    background: linear-gradient(135deg, {COLOR_001D39} 0%, {COLOR_0A4174} 50%, {COLOR_49769F} 100%);
    border-radius: 24px;
    padding: 48px 40px;
    color: #FFFFFF;
    box-shadow: 0 16px 40px rgba(0, 29, 57, 0.16);
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
    background: radial-gradient(circle, {COLOR_7BBDE8} 0%, transparent 70%);
    opacity: 0.3;
    pointer-events: none;
}}

.intro-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: var(--radius-pill);
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    font-size: 11px;
    font-weight: 700;
    color: {COLOR_7BBDE8};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 18px;
}}

.intro-feature-card {{
    background: #FFFFFF;
    border: 1px solid {COLOR_BDD8E9};
    border-radius: var(--radius-card);
    padding: 24px;
    height: 100%;
    box-shadow: var(--shadow-soft);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}

.intro-feature-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0, 29, 57, 0.12);
    border-color: {COLOR_6EA2B3};
}}

.intro-stat-box {{
    background: #F0F6FA;
    border: 1px solid {COLOR_BDD8E9};
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}}

/* Success Checkmark Icon Fix */
.checkmark-circle {{
    width: 56px !important;
    height: 56px !important;
    max-width: 56px !important;
    max-height: 56px !important;
    border-radius: 50% !important;
    background: #E7F8F0 !important;
    border: 2px solid #1E9E6B !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto 10px auto !important;
    box-shadow: 0 4px 12px rgba(30, 158, 107, 0.15) !important;
}}

.checkmark-icon {{
    width: 26px !important;
    height: 26px !important;
    max-width: 26px !important;
    max-height: 26px !important;
    stroke: #1E9E6B !important;
    stroke-width: 3 !important;
    fill: none !important;
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
    dot_color = COLOR_49769F
    
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
        color = COLOR_49769F
        bg_track = COLOR_BDD8E9
        status_text = "Reconciliation Required"

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
                <span style="font-size: 22px; font-weight: 700; color: {COLOR_001D39}; font-family: 'Inter', sans-serif;">{score}</span>
                <span style="font-size: 10px; color: {COLOR_49769F}; font-weight: 600; text-transform: uppercase;">Score</span>
            </div>
        </div>
        <div style="font-size: 12px; font-weight: 600; color: {color}; margin-top: 8px;">{status_text}</div>
    </div>
    '''

def render_money_text(amount: float, currency: str = "₹", size: str = "28px", label: str = None) -> str:
    """Renders formatted money text with clean typography."""
    formatted = f"{amount:,.2f}"
    sub = f'<div style="font-size: 12px; color: {COLOR_49769F}; margin-top: 4px;">{label}</div>' if label else ""
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
