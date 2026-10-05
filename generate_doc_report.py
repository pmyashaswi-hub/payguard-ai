"""
Python script to generate a styled Microsoft Word (.docx) Project Report for PayGuard AI.
Follows the reference report layout with headers, tables, bullet points, and styled callout boxes.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles & Colors
    NAVY_HEX = "001D39"
    BLUE_HEX = "0A4174"
    LIGHT_BG_HEX = "F0F6FA"
    BORDER_HEX = "BDD8E9"

    NAVY_RGB = RGBColor(0, 29, 57)
    BLUE_RGB = RGBColor(10, 65, 116)
    DARK_RGB = RGBColor(30, 41, 59)

    # Title Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_title = p_title.add_run("PROJECT REPORT")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY_RGB

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("PayGuard AI — Intelligent Payment Protection & Real-Time Fraud Detection System")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = BLUE_RGB

    doc.add_paragraph()

    # Metadata Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    meta_data = [
        ("Your Name", ": Full-Stack & AI Developer"),
        ("Your Role", ": Lead AI & Software Engineer"),
        ("Project Name", ": PayGuard AI --- Intelligent Payment Protection System"),
        ("Team Members", ": Development Team")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl = row.cells[0]
        cell_val = row.cells[1]
        
        p_l = cell_lbl.paragraphs[0]
        r_l = p_l.add_run(label)
        r_l.font.name = "Arial"
        r_l.font.size = Pt(10.5)
        r_l.font.bold = True
        r_l.font.color.rgb = NAVY_RGB
        
        p_v = cell_val.paragraphs[0]
        r_v = p_v.add_run(val)
        r_v.font.name = "Arial"
        r_v.font.size = Pt(10.5)
        r_v.font.color.rgb = DARK_RGB

        set_cell_margins(cell_lbl, top=60, bottom=60, left=60, right=60)
        set_cell_margins(cell_val, top=60, bottom=60, left=60, right=60)

    doc.add_paragraph()

    # Helper function for Section Headings
    def add_section_heading(num_str, title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r_num = p.add_run(f"{num_str}  ")
        r_num.font.name = "Arial"
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        r_num.font.color.rgb = BLUE_RGB

        r_txt = p.add_run(title_str.upper())
        r_txt.font.name = "Arial"
        r_txt.font.size = Pt(12)
        r_txt.font.bold = True
        r_txt.font.color.rgb = NAVY_RGB

    def add_sub_heading(title_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_str)
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = BLUE_RGB

    def add_body_p(text_str):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text_str)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_RGB
        return p

    def add_bullet_p(title_str, text_str):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(f"{title_str}: ")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = NAVY_RGB

        r_v = p.add_run(text_str)
        r_v.font.name = "Arial"
        r_v.font.size = Pt(10)
        r_v.font.color.rgb = DARK_RGB

    # 01 SYSTEM OVERVIEW
    add_section_heading("01", "SYSTEM OVERVIEW")
    add_body_p(
        "PayGuard AI is an intelligent, real-time payment security and fraud detection system designed to evaluate online financial transactions, prevent fraudulent transfers, and protect user accounts. "
        "It evaluates submitted transactions using a PyTorch ResNeXt-GRU deep learning model in under 50ms latency, computing a continuous fraud probability score (0–100) and categorizing transactions into three automated decision bands: ALLOW (0-30 score, Low Risk), VERIFY (31-70 score, Step-Up 4-Digit UPI PIN Verification), and REVIEW (71-100 score, High Risk Payment Blockage). "
        "The system incorporates Clerk Auth Engine (clerk.com) and real SMTP email OTP verification for secure user onboarding, alongside a double-entry reconciliation ledger in SQLite (payguard_bank.db)."
    )

    # 02 SYSTEM ARCHITECTURE & COMPONENTS
    add_section_heading("02", "SYSTEM ARCHITECTURE & COMPONENTS")
    add_sub_heading("2.1 System Architecture")
    add_body_p(
        "PayGuard AI follows a modular Client-Server Architecture consisting of a Streamlit Single-Page Application (SPA) frontend, a FastAPI REST backend engine, a PyTorch spatial-temporal ResNeXt-GRU neural network, a persistent SQLite database (payguard_bank.db), and an external Clerk Authentication service."
    )

    add_sub_heading("2.2 Frontend Components (Streamlit SPA)")
    add_bullet_p("App Routing & Navigation", "Manages reactive tab routing, active user session card, and real-time FastAPI engine health telemetry.")
    add_bullet_p("Project Overview / Intro", "Zero-scroll full-screen landing overview featuring dot-grid canvas background, core metrics, and action pills.")
    add_bullet_p("Profile & Authentication", "Dual-mode Log In (Mail ID + Password) & Two-Stage Create Account (Clerk Mail Verification + Password & 4-Digit UPI PIN setup).")
    add_bullet_p("Home / Wallet Dashboard", "Displays real-time wallet balances (default ₹50,000.00), account details, recent activity, and security status.")
    add_bullet_p("Payment Flow Wizard", "3-step transaction wizard: Details Entry -> ResNeXt-GRU AI Risk Evaluation -> 4-Digit UPI PIN Authorization & Balance Transfer.")
    add_bullet_p("Transaction History", "Searchable and filterable audit trail displaying risk levels, decision tags (ALLOW/VERIFY/REVIEW), and CSV export.")
    add_bullet_p("Security Center", "Real-time AI model telemetry, layer architecture breakdown, feature importance metrics, and active security rules.")
    add_bullet_p("Database Inspector", "In-app GUI table viewer for real-time inspection of users, beneficiaries, transactions, and security logs.")

    add_sub_heading("2.3 Backend Components (FastAPI & PyTorch Engine)")
    add_bullet_p("FastAPI REST Engine", "Exposes asynchronous endpoints (/api/v1/predict, /api/v1/health) handling CORS, request validation, and sub-50ms inference.")
    add_bullet_p("ResNeXt-GRU PyTorch Model", "Combines 3D Convolutional ResNeXt backbone for spatial feature extraction with Gated Recurrent Units (GRU) for sequence fraud modeling.")
    add_bullet_p("Database Manager Layer", "Handles SQLite connection pooling, schema migrations, SHA-256 password & UPI PIN hashing, and default seed accounts.")

    add_sub_heading("2.4 Data and External Services")
    add_bullet_p("Clerk Auth Engine", "Provides user identity management, Clerk API authentication (CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY), and dashboard app linking.")
    add_bullet_p("Real SMTP Email Dispatch", "Dispatches 6-digit email confirmation codes directly to recipient email inboxes via TLS/SSL.")
    add_bullet_p("SQLite Database", "Stores persistent user records, hashed credentials, payee lists, and transaction audit trails in payguard_bank.db.")

    # 03 SYSTEM WORKFLOW
    add_section_heading("03", "SYSTEM WORKFLOW")
    add_bullet_p("1. User Input", "User enters payment details (Recipient Name/UPI ID, Amount, Purpose).")
    add_bullet_p("2. Telemetry Extraction", "System extracts transaction metadata (Amount, Device IP, Velocity, Location Anomaly).")
    add_bullet_p("3. FastAPI AI Inference", "Telemetry is transmitted to /api/v1/predict and evaluated by PyTorch ResNeXt-GRU model in < 50ms.")
    add_bullet_p("4. Decision Band Assignment", "Evaluates risk score (0–100) and assigns ALLOW, VERIFY, or REVIEW decision tag.")
    add_bullet_p("5. 4-Digit UPI PIN Authorization", "User authorizes transaction using their registered 4-digit UPI PIN verified against SHA-256 database hash.")
    add_bullet_p("6. Data Storage & Ledger Sync", "Balance is atomically updated and transaction audit record is saved in SQLite database.")

    # 04 DATABASE DESIGN
    add_section_heading("04", "DATABASE DESIGN")
    add_body_p(
        "PayGuard AI uses SQLite (payguard_bank.db) for persistent data storage. Main entities include:"
    )
    add_bullet_p("users Table", "Stores user_id, name, mobile, email, pin_hash (SHA-256), password_hash (SHA-256), account_number, upi_id, available_balance, and security_score.")
    add_bullet_p("beneficiaries Table", "Stores payee records (id, user_id, name, email, upi_id, account_num, avatar_bg, initials, trusted).")
    add_bullet_p("transactions Table", "Stores completed transfers (tx_id, user_id, recipient, amount, status, decision, risk_score, fraud_risk_pct, JSON security_signals, timeline).")
    add_bullet_p("security_events Table", "Logs system security alerts, PIN attempt failures, and model inference audit logs.")

    # 05 TECHNOLOGY STACK
    add_section_heading("05", "TECHNOLOGY STACK")
    
    tech_table = doc.add_table(rows=10, cols=2)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Category", "Technology"]
    hdr_cells = tech_table.rows[0].cells
    for i, h_text in enumerate(headers):
        p = hdr_cells[i].paragraphs[0]
        r = p.add_run(h_text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(hdr_cells[i], NAVY_HEX)
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=150, right=150)

    tech_rows = [
        ("Frontend Framework", "Streamlit (Python Single-Page Application)"),
        ("Styling & UI", "HTML5, Custom CSS3 Design Tokens (Oceanic Blue Palette)"),
        ("Backend Framework", "Python 3.14, FastAPI, Uvicorn"),
        ("AI / ML Framework", "PyTorch (ResNeXt-GRU Spatial-Temporal Deep Learning)"),
        ("Database", "SQLite (payguard_bank.db), SQLAlchemy / SQLite3"),
        ("Cryptographic Hashing", "SHA-256 (Passwords & 4-Digit UPI PINs)"),
        ("Authentication Engine", "Clerk Auth Engine (clerk.com), clerk-backend-api"),
        ("Email Dispatch", "Python smtplib (SMTP over TLS/SSL)"),
        ("Automated Testing", "Python unittest, custom test scripts (test_email_password_auth.py)")
    ]

    for idx, (cat, tech) in enumerate(tech_rows):
        row_cells = tech_table.rows[idx + 1].cells
        
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(cat)
        r0.font.name = "Arial"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = NAVY_RGB

        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(tech)
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = DARK_RGB

        bg_color = LIGHT_BG_HEX if idx % 2 == 1 else "FFFFFF"
        set_cell_background(row_cells[0], bg_color)
        set_cell_background(row_cells[1], bg_color)
        set_cell_margins(row_cells[0], top=80, bottom=80, left=120, right=120)
        set_cell_margins(row_cells[1], top=80, bottom=80, left=120, right=120)

    doc.add_paragraph()

    # 06 DEPLOYMENT & VERIFICATION ARCHITECTURE
    add_section_heading("06", "DEPLOYMENT & VERIFICATION ARCHITECTURE")
    add_body_p(
        "PayGuard AI uses a distributed microservice architecture: Browser -> Streamlit Frontend (Port 8501) -> FastAPI REST Backend Engine (Port 8000) -> SQLite Database (payguard_bank.db) & Clerk Auth API (api.clerk.com)."
    )
    add_bullet_p("Automated Verification", "Verified by comprehensive test scripts (tests/test_email_password_auth.py and tests/test_clerk_auth_flow.py) ensuring 100% pass rates across password hashing, UPI PIN validation, Clerk API linking, and transaction ledgering.")

    # 07 CONCLUSION
    add_section_heading("07", "CONCLUSION")
    add_body_p(
        "PayGuard AI provides an integrated, military-grade payment protection system combining PyTorch ResNeXt-GRU AI risk evaluation, Clerk / SMTP email verification, 4-digit UPI PIN authorization, and persistent SQLite database ledgering. "
        "Its architecture effectively separates frontend presentation, REST API engine processing, deep learning model evaluation, and secure database persistence to achieve real-time payment fraud prevention in under 50ms."
    )

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PayGuard_AI_Project_Report.docx")
    doc.save(out_path)
    print(f"Successfully generated DOCX project report at: {out_path}")

if __name__ == "__main__":
    create_report()
