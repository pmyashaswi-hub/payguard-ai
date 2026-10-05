"""
Script to generate PayGuard_AI_Backend_Project_Report_Clear.docx with professional Vamscore styling.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.bold = True
    if level == 1:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(11, 29, 51) # Dark Navy #0B1D33
    elif level == 2:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(10, 65, 116) # Royal Blue #0A4174
    return p

def generate_report():
    doc = docx.Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # ---------------------------------------------------------
    # HEADER / BRANDING
    # ---------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    cell_left = header_table.cell(0, 0)
    cell_right = header_table.cell(0, 1)

    p_logo = cell_left.paragraphs[0]
    r_brand = p_logo.add_run("Vamscore ")
    r_brand.font.name = 'Arial'
    r_brand.font.size = Pt(28)
    r_brand.font.bold = True
    r_brand.font.color.rgb = RGBColor(139, 92, 246) # Purple #8B5CF6

    p_contact = cell_right.paragraphs[0]
    p_contact.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_c = p_contact.add_run("📞 +91 9490729484\n✉ info@vamscore.com\n🌐 www.vamscore.com")
    r_c.font.name = 'Arial'
    r_c.font.size = Pt(9.5)
    r_c.font.color.rgb = RGBColor(73, 118, 159) # Slate #49769F

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("PROJECT REPORT")
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(22)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(11, 29, 51)

    # Metadata Grid
    meta_table = doc.add_table(rows=4, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Your Name", ":", "Shravya K"),
        ("Your Role", ":", "Main Backend Developer"),
        ("Project Name", ":", "Online Payment Fraud Detection Using ML (PayGuard AI)"),
        ("Team Members", ":", "Yashaswi PM, Ravi Kumar G, Sinchana K")
    ]
    for idx, (k, col, v) in enumerate(meta_data):
        row = meta_table.rows[idx]
        rk = row.cells[0].paragraphs[0].add_run(k)
        rk.font.name = 'Arial'
        rk.font.bold = True
        rk.font.size = Pt(10.5)
        rk.font.color.rgb = RGBColor(11, 29, 51)

        rc = row.cells[1].paragraphs[0].add_run(col)
        rc.font.name = 'Arial'
        rc.font.size = Pt(10.5)

        rv = row.cells[2].paragraphs[0].add_run(v)
        rv.font.name = 'Arial'
        rv.font.size = Pt(10.5)
        rv.font.color.rgb = RGBColor(10, 65, 116)
        if k == "Your Role":
            rv.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ---------------------------------------------------------
    # SECTION 01: ABOUT THE PROJECT
    # ---------------------------------------------------------
    add_heading_styled(doc, "01   ABOUT THE PROJECT", level=1)
    p_about = doc.add_paragraph()
    p_about.paragraph_format.space_after = Pt(10)
    p_about.paragraph_format.line_spacing = 1.15
    r_ab = p_about.add_run(
        "PayGuard AI is an enterprise-grade, real-time payment fraud detection and ledger security system. "
        "The backend microservice analyzes transaction telemetry, device fingerprints, geographic shifts, velocity spikes, "
        "and payment gateway ledger consistency. Using a hybrid PyTorch RXT deep learning model (ResNeXt + GRU) and an automated "
        "Risk Engine, the system computes authentic 0–100 risk scores and triggers automated security decisions (ALLOW, VERIFY, or REVIEW)."
    )
    r_ab.font.name = 'Arial'
    r_ab.font.size = Pt(10.5)
    r_ab.font.color.rgb = RGBColor(51, 65, 85)

    # ---------------------------------------------------------
    # SECTION 02: YOUR ROLE IN THE PROJECT
    # ---------------------------------------------------------
    add_heading_styled(doc, "02   YOUR ROLE IN THE PROJECT", level=1)
    p_role = doc.add_paragraph()
    p_role.paragraph_format.space_after = Pt(10)
    r_r = p_role.add_run("Worked as the Main Backend Developer, responsible for designing, building, hardening, and deploying:")
    r_r.font.name = 'Arial'
    r_r.font.size = Pt(10.5)

    role_items = [
        "FastAPI REST microservice exposing health monitoring (/api/v1/health) and fraud prediction (/api/v1/predict) APIs.",
        "PyTorch RXT deep learning model combining ResNeXt 1D grouped convolutions and GRU temporal sequence processing.",
        "Dynamic 16-dimensional telemetry preprocessing pipeline and continuous logistic sigmoid probability calibration.",
        "Risk Engine decision matrix mapping continuous risk scores to decision tiers (ALLOW, VERIFY, REVIEW).",
        "Dual-engine transactional email infrastructure (Resend REST API + Gmail SMTP Fallback) for real-time Step-Up OTP verification.",
        "Real-time SQLite database persistence layer (payguard_bank.db) logging transactions, ledger reconciliation events, and wallet top-ups."
    ]
    for ri in role_items:
        p_item = doc.add_paragraph(style='List Bullet')
        p_item.paragraph_format.space_after = Pt(4)
        r_item = p_item.add_run(ri)
        r_item.font.name = 'Arial'
        r_item.font.size = Pt(10)
        r_item.font.color.rgb = RGBColor(30, 41, 59)

    # ---------------------------------------------------------
    # SECTION 03: TOOLS & TECHNOLOGIES USED
    # ---------------------------------------------------------
    add_heading_styled(doc, "03   TOOLS & TECHNOLOGIES USED", level=1)

    tools_table = doc.add_table(rows=8, cols=2)
    tools_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tools_data = [
        ("Programming Language", "Python 3.14"),
        ("API Framework", "FastAPI, Uvicorn, Pydantic v2"),
        ("Deep Learning Engine", "PyTorch (torch.nn, 1D Grouped Convolutions, GRU)"),
        ("Data Processing", "NumPy, Pandas, Scikit-learn, Joblib"),
        ("Dataset Benchmark", "IEEE-CIS Fraud Detection Dataset"),
        ("Database & Storage", "SQLite3 (payguard_bank.db)"),
        ("Email & Auth Security", "Resend API (api.resend.com), Gmail SMTP (smtplib), SHA-256 (hashlib)"),
        ("Deployment & Testing", "Pytest, Streamlit In-Process Integration Engine")
    ]
    # Header Row
    hdr_cells = tools_table.rows[0].cells
    hdr_cells[0].paragraphs[0].add_run("Category").font.bold = True
    hdr_cells[1].paragraphs[0].add_run("Tools & Libraries").font.bold = True
    for c in hdr_cells:
        set_cell_background(c, "0A4174")
        for p in c.paragraphs:
            p.runs[0].font.name = 'Arial'
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            p.runs[0].font.size = Pt(10)

    for idx, (cat, val) in enumerate(tools_data):
        row_cells = tools_table.rows[idx].cells
        row_cells[0].paragraphs[0].add_run(cat).font.name = 'Arial'
        row_cells[1].paragraphs[0].add_run(val).font.name = 'Arial'
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(row_cells[0], bg)
        set_cell_background(row_cells[1], bg)
        for rc in row_cells:
            set_cell_margins(rc, top=100, bottom=100, left=150, right=150)
            for p in rc.paragraphs:
                p.runs[0].font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ---------------------------------------------------------
    # SECTION 04: COMPLETE BACKEND ACCOMPLISHMENTS
    # ---------------------------------------------------------
    add_heading_styled(doc, "04   COMPLETE BACKEND ACCOMPLISHMENTS (WHAT HAS BEEN DONE TILL NOW)", level=1)

    accs = [
        ("1. FastAPI Microservice & API Contracts", [
            "Developed /api/v1/health endpoint for system health monitoring and /api/v1/predict for real-time fraud prediction.",
            "Built Pydantic v2 validation schemas enforcing data types for amounts, card features, email domains, device telemetry, and ledger status.",
            "Configured CORS policies in main.py to enable seamless frontend integration."
        ]),
        ("2. PyTorch RXT Neural Model & Trained Weights", [
            "Implemented hybrid ResNeXt1DBlock (grouped convolutions g=4) combined with a 2-layer GRU sequence processor in rxt.py.",
            "Trained and saved PyTorch neural weights file to rxt_model.pt.",
            "Refactored predictor.py to remove static threshold floats (0.784, 0.348, 0.084) and static vector padding, enabling continuous mathematical probability predictions."
        ]),
        ("3. Dynamic 16-Dimensional Telemetry Preprocessing", [
            "Built _preprocess() in predictor.py to normalize 16 live telemetry features:",
            "• Amount ratio, failed PIN attempts ratio, new device flag, new location flag, velocity spike.",
            "• Card metrics (card1, card2), billing region (addr1), distance metric (dist1), sliding window count (recent_transactions).",
            "• Email domain trust scores (p_emaildomain, r_emaildomain), device platform risk (device_type), ledger debits/credits, and gateway status."
        ]),
        ("4. Risk Engine & Pure Behavioral Decision Tiers", [
            "Refactored risk_engine.py so Risk Scores (0–100) reflect pure ML model output and behavioral signals without artificial score mutation.",
            "Decision Tiers: ALLOW (Score <= 25), VERIFY (Score 26–65), REVIEW (Score > 65).",
            "1 Lakh Policy Guardrail: Implemented an independent limit check (limit_exceeded: True/False) for transfers exceeding ₹1,00,000 (1 Lakh)."
        ]),
        ("5. Dual-Engine Email OTP Infrastructure (Resend API + Gmail SMTP)", [
            "Integrated Resend REST API (https://api.resend.com/emails) for instant OTP code dispatch.",
            "Built automatic fallback to Gmail SMTP (smtp.gmail.com) when operating in sandbox mode, ensuring 100% email delivery.",
            "Ensured 6-digit OTP codes are delivered exclusively to the user's email inbox without displaying them on the web interface.",
            "Resolved duplicate email generation bugs during user registration."
        ]),
        ("6. Real-Time Ledger Persistence & Reconciliation Logging", [
            "Implemented ledger inconsistency detection between payment gateway and settlement ledger.",
            "Updated mock_transaction_service.py with deduct_balance=False support.",
            "Reconciliation Required and Security Review Blocked events are written directly to SQLite database payguard_bank.db in real time."
        ]),
        ("7. Real-Time Wallet Balance Top-Up Engine", [
            "Added top_up_user_balance() in database.py to process dynamic wallet top-ups (+₹1,000, +₹5,000, +₹10,000, or custom amounts).",
            "Updates available balance in SQLite database payguard_bank.db in real time."
        ]),
        ("8. Cryptographic Security Hardening", [
            "Removed hardcoded PIN fallback checks (elif pin in ['1234', '5678']) in database.py.",
            "Enforced strict SHA-256 password and PIN hash validation for all user authentication requests."
        ])
    ]

    for title, bullet_list in accs:
        add_heading_styled(doc, title, level=2)
        for b in bullet_list:
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_after = Pt(3)
            r_b = p_b.add_run(b)
            r_b.font.name = 'Arial'
            r_b.font.size = Pt(9.5)
            r_b.font.color.rgb = RGBColor(30, 41, 59)

    # ---------------------------------------------------------
    # SECTION 05: SUMMARY OF VERIFIED SYSTEM BENCHMARKS
    # ---------------------------------------------------------
    add_heading_styled(doc, "05   SUMMARY OF VERIFIED SYSTEM BENCHMARKS", level=1)

    bench_table = doc.add_table(rows=5, cols=2)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_data = [
        ("API Health Check (/api/v1/health)", "Status: Healthy (200 OK) | Model Version: RXT-ResNeXt-GRU-v1.2"),
        ("Normal Transfer (Score 4)", "Decision: ALLOW -> Instant Payment Executed"),
        ("Medium Risk Transfer (Score 54)", "Decision: VERIFY -> Real-Time Email OTP Code Sent"),
        ("High Risk Transfer (Score 83)", "Decision: REVIEW -> Security Review Blocked (Funds Retained)"),
        ("Transaction Limit & Ledger Check", "Single Transfer > 1 Lakh -> limit_exceeded: True | Mismatch -> Reconciliation Required (Saved in DB)")
    ]
    for idx, (k, v) in enumerate(b_data):
        row_cells = bench_table.rows[idx].cells
        row_cells[0].paragraphs[0].add_run(k).font.bold = True
        row_cells[1].paragraphs[0].add_run(v)
        bg = "F1F5F9" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(row_cells[0], bg)
        set_cell_background(row_cells[1], bg)
        for rc in row_cells:
            set_cell_margins(rc, top=100, bottom=100, left=150, right=150)
            for p in rc.paragraphs:
                p.runs[0].font.name = 'Arial'
                p.runs[0].font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Conclusion Badge
    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.space_before = Pt(10)
    r_conc = p_conc.add_run("✅ ALL BACKEND MODULES, DEEP LEARNING MODELS, SECURITY ENGINES, AND DATABASE PERSISTENCE LAYERS HAVE BEEN HARDENED AND VERIFIED WITH 100% CLEAN TEST EXECUTION.")
    r_conc.font.name = 'Arial'
    r_conc.font.bold = True
    r_conc.font.size = Pt(10)
    r_conc.font.color.rgb = RGBColor(30, 126, 85)

    out_path = os.path.join(os.path.dirname(__file__), "PayGuard_AI_Backend_Project_Report_Clear.docx")
    doc.save(out_path)
    print(f"Successfully generated Word document report at: {out_path}")

if __name__ == "__main__":
    generate_report()
