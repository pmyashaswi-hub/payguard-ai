"""
PayGuard AI - Vamscore Format Frontend Project Report Generator.
Builds a styled Microsoft Word (.docx) matching the exact Vamscore Project Report format for Frontend Developer role,
featuring a high-resolution, full-page landscape diagram section for crystal-clear readability.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_PATH_1 = r"C:\Users\ASUS\.gemini\antigravity\scratch\payguard-ai\PayGuard_AI_Vamscore_Frontend_Project_Report.docx"
OUTPUT_PATH_2 = r"C:\Users\ASUS\.gemini\antigravity\scratch\PayGuard_AI_Vamscore_Frontend_Project_Report.docx"

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_vamscore_header(doc):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell_l = tbl.cell(0, 0)
    cell_l.width = Inches(3.5)
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_logo = p_l.add_run("Vamscore")
    r_logo.bold = True
    r_logo.font.size = Pt(28)
    r_logo.font.color.rgb = RGBColor(142, 36, 170)
    
    cell_r = tbl.cell(0, 1)
    cell_r.width = Inches(3.0)
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    r_cnt = p_r.add_run("📞 +91 9490729484\n✉ info@vamscore.com\n🌐 www.vamscore.com")
    r_cnt.font.size = Pt(9.5)
    r_cnt.font.color.rgb = RGBColor(51, 51, 51)
    
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(4)
    p_div.paragraph_format.space_after = Pt(14)
    p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="8E24AA"/></w:pBdr>')
    p_div._p.get_or_add_pPr().append(p_div_border)

def add_section_header(doc, num_str, title_str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    
    run_num = p.add_run(f"{num_str}   ")
    run_num.bold = True
    run_num.font.size = Pt(14)
    run_num.font.color.rgb = RGBColor(142, 36, 170)
    
    run_title = p.add_run(title_str.upper())
    run_title.bold = True
    run_title.font.size = Pt(14)
    run_title.font.color.rgb = RGBColor(0, 29, 57)

def format_table_headers(tbl, col_widths, headers):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = tbl.rows[0].cells
    for idx, text in enumerate(headers):
        hdr_cells[idx].text = text
        set_cell_background(hdr_cells[idx], "8E24AA")
        set_cell_margins(hdr_cells[idx], top=120, bottom=120, left=140, right=140)
        hdr_cells[idx].width = Inches(col_widths[idx])
        
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(10)
            run.font.color.rgb = RGBColor(255, 255, 255)

def build_vamscore_report():
    print("Building Vamscore Format Frontend Project Report with HD Landscape Diagram...")
    doc = Document()

    sec_main = doc.sections[0]
    sec_main.top_margin = Inches(0.8)
    sec_main.bottom_margin = Inches(0.8)
    sec_main.left_margin = Inches(0.8)
    sec_main.right_margin = Inches(0.8)

    add_vamscore_header(doc)

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("PROJECT REPORT")
    r_t.bold = True
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = RGBColor(0, 29, 57)

    # Metadata Block
    meta_items = [
        ("Your Name", "Yashaswi PM"),
        ("Your Role", "Frontend Developer"),
        ("Project Name", "Online Payment Fraud Detection Using ML"),
        ("Team Members", "Yashaswi PM, Ravi Kumar G, Sinchana K, Shravya K")
    ]
    
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.LEFT
    for idx, (k, v) in enumerate(meta_items):
        r = tbl_meta.rows[idx]
        cell_k, cell_v = r.cells[0], r.cells[1]
        cell_k.width = Inches(1.8)
        cell_v.width = Inches(4.7)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_before = Pt(2)
        pk.paragraph_format.space_after = Pt(2)
        rk = pk.add_run(f"{k}  :")
        rk.bold = True
        rk.font.size = Pt(11)
        rk.font.color.rgb = RGBColor(0, 29, 57)
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_before = Pt(2)
        pv.paragraph_format.space_after = Pt(2)
        rv = pv.add_run(v)
        rv.font.size = Pt(11)
        rv.font.color.rgb = RGBColor(51, 51, 51)
        if k == "Your Role":
            rv.bold = True
            rv.font.color.rgb = RGBColor(142, 36, 170)

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_after = Pt(8)

    # 01 ABOUT THE PROJECT
    add_section_header(doc, "01", "ABOUT THE PROJECT")
    p_ab = doc.add_paragraph()
    p_ab.paragraph_format.space_after = Pt(10)
    p_ab.add_run(
        "Developed an Online Payment Fraud Detection single-page web frontend application using Streamlit and Python to deliver a "
        "responsive, zero-scroll digital wallet interface (PayGuard AI). The frontend handles user authentication, multi-step Clerk OTP email "
        "verification, dynamic frequent payee management, real-time risk score visualization, and step-up UPI PIN authorization in under 50ms latency."
    ).font.color.rgb = RGBColor(51, 51, 51)

    # 02 SYSTEM DESIGN (PORTRAIT INTRO + LANDSCAPE HIGH-RES DIAGRAM PAGE)
    add_section_header(doc, "02", "SYSTEM DESIGN")
    p_sd = doc.add_paragraph()
    p_sd.paragraph_format.space_after = Pt(6)
    p_sd.add_run("The high-resolution sequence diagram on the following page details the Frontend System Architecture across all 5 operational phases (App Initialization, Two-Stage Registration Wizard with Clerk OTP, Login Authentication, Money Transfer with Real-Time AI Fraud Check, and Step-Up PIN Authorization & Ledger Sync):")

    # Add LANDSCAPE section for crystal-clear diagram display
    sec_diag = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_diag.orientation = WD_ORIENT.LANDSCAPE
    sec_diag.page_width = Inches(11.0)
    sec_diag.page_height = Inches(8.5)
    sec_diag.top_margin = Inches(0.5)
    sec_diag.bottom_margin = Inches(0.5)
    sec_diag.left_margin = Inches(0.6)
    sec_diag.right_margin = Inches(0.6)

    add_section_header(doc, "02.1", "FRONTEND OPERATIONAL SEQUENCE WORKFLOW DIAGRAM (FULL PAGE HD)")
    
    img_hd_path = r"C:\Users\ASUS\.gemini\antigravity\scratch\payguard-ai\PayGuard_AI_Frontend_Clear_Workflow.png"
    if os.path.exists(img_hd_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        # Max width 9.5 inches on landscape page for maximum clarity
        p_img.add_run().add_picture(img_hd_path, width=Inches(9.4))

    # Switch back to PORTRAIT section for remaining text & tables
    sec_port = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_port.orientation = WD_ORIENT.PORTRAIT
    sec_port.page_width = Inches(8.5)
    sec_port.page_height = Inches(11.0)
    sec_port.top_margin = Inches(0.8)
    sec_port.bottom_margin = Inches(0.8)
    sec_port.left_margin = Inches(0.8)
    sec_port.right_margin = Inches(0.8)

    # 03 TOOLS YOU USED
    add_section_header(doc, "03", "TOOLS YOU USED")
    
    tools_headers = ["Technology", "Purpose"]
    tools_widths = [2.2, 4.3]
    tbl_tools = doc.add_table(rows=1, cols=2)
    format_table_headers(tbl_tools, tools_widths, tools_headers)

    tools_data = [
        ("Python", "Main frontend integration and logic programming language"),
        ("Streamlit", "Modern single-page web interface framework for real-time UI rendering"),
        ("Clerk API / SMTP", "Identity verification and 6-digit OTP email code dispatch service"),
        ("SQLite3 (payguard_bank.db)", "Relational database storage for users, payees, transactions, and audit logs"),
        ("Hashlib (SHA-256)", "Cryptographic hashing for user passwords and 4-digit UPI PIN isolation"),
        ("Requests (HTTP REST)", "Async/sync API client connecting frontend UI with FastAPI PyTorch backend"),
        ("Pandas & Datetime", "Ledger transaction filtering, timestamp formatting, and table telemetry"),
        ("Custom CSS (Oceanic Navy)", "Viewport optimization ensuring zero vertical scrolling across screens")
    ]

    for row_idx, (tech, purp) in enumerate(tools_data):
        row = tbl_tools.add_row()
        bg = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
        
        c0, c1 = row.cells[0], row.cells[1]
        c0.text, c1.text = tech, purp
        c0.width, c1.width = Inches(tools_widths[0]), Inches(tools_widths[1])
        
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_margins(c0, top=100, bottom=100, left=120, right=120)
        set_cell_margins(c1, top=100, bottom=100, left=120, right=120)
        
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        p0.runs[0].font.bold = True
        p0.runs[0].font.size = Pt(9.5)
        p0.runs[0].font.color.rgb = RGBColor(0, 29, 57)
        p1.runs[0].font.size = Pt(9.5)
        p1.runs[0].font.color.rgb = RGBColor(51, 51, 51)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(10)

    # 04 FRONTEND COMPONENTS
    add_section_header(doc, "04", "FRONTEND COMPONENTS")

    # 4.1
    p_41 = doc.add_paragraph()
    p_41.paragraph_format.space_before = Pt(4)
    p_41.paragraph_format.space_after = Pt(4)
    r_41 = p_41.add_run("4.1 Streamlit Router & Oceanic Navy Theme Engine")
    r_41.bold = True
    r_41.font.size = Pt(11.5)
    r_41.font.color.rgb = RGBColor(142, 36, 170)

    p_41_b = doc.add_paragraph()
    p_41_b.add_run(
        "• The main entry point (streamlit_app.py) initializes global session state (st.session_state) and injects responsive CSS styling.\n"
        "• Provides a top navigation header with wallet balance pills, active user metadata, and instant screen switching without full browser reloads."
    )

    # 4.2
    p_42 = doc.add_paragraph()
    p_42.paragraph_format.space_before = Pt(8)
    p_42.paragraph_format.space_after = Pt(4)
    r_42 = p_42.add_run("4.2 Auth UI & Two-Stage Registration Wizard (Clerk OTP)")
    r_42.bold = True
    r_42.font.size = Pt(11.5)
    r_42.font.color.rgb = RGBColor(142, 36, 170)

    p_42_b = doc.add_paragraph()
    p_42_b.add_run(
        "• Step 1 (Identity & Clerk Verification): Collects Full Name, 10-digit Mobile Number, and Email ID. Dispatches 6-digit OTP code to email inbox via Clerk API / SMTP.\n"
        "• Step 2 (Security Credentials Next Page): Dedicated second page screen collects Password (min 8 chars) and 4-Digit UPI PIN. Hashes credentials using SHA-256 and executes UPSERT into SQLite payguard_bank.db."
    )

    # 4.3
    p_43 = doc.add_paragraph()
    p_43.paragraph_format.space_before = Pt(8)
    p_43.paragraph_format.space_after = Pt(4)
    r_43 = p_43.add_run("4.3 Payment UI & Dynamic Frequent Payees")
    r_43.bold = True
    r_43.font.size = Pt(11.5)
    r_43.font.color.rgb = RGBColor(142, 36, 170)

    p_43_b = doc.add_paragraph()
    p_43_b.add_run(
        "• Dynamic Clean Slate: Newly registered users start with an empty frequent payees list ([]). No mock or hardcoded fake beneficiaries are shown.\n"
        "• Auto-Save Payee Engine: Upon successful payment completion, the payee is automatically added or marked as frequent (is_frequent = 1) in payguard_bank.db for instant quick-tap transfers on future visits."
    )

    # 4.4
    p_44 = doc.add_paragraph()
    p_44.paragraph_format.space_before = Pt(8)
    p_44.paragraph_format.space_after = Pt(4)
    r_44 = p_44.add_run("4.4 Real-Time AI Fraud Risk Engine & Step-Up Email OTP Verification")
    r_44.bold = True
    r_44.font.size = Pt(11.5)
    r_44.font.color.rgb = RGBColor(142, 36, 170)

    p_44_b = doc.add_paragraph()
    p_44_b.add_run(
        "• Intercepts transfers by sending transaction features (user_id, recipient, amount, device, location) to FastAPI backend (/analyze-risk).\n"
        "• Evaluates PyTorch ResNeXt-GRU model risk score (0-100):\n"
        "  - Score 0 to 25 (ALLOW): Instant payment execution.\n"
        "  - Score 26 to 65 (VERIFY): Automatically dispatches a real-time 6-digit OTP code to the user's registered Mail ID via Clerk Auth & SMTP Engine for step-up two-factor authorization.\n"
        "  - Score 66 to 100 (REVIEW): High-risk transaction blocked & security audit event recorded."
    )

    # 4.5
    p_45 = doc.add_paragraph()
    p_45.paragraph_format.space_before = Pt(8)
    p_45.paragraph_format.space_after = Pt(4)
    r_45 = p_45.add_run("4.5 Ledger Screen & Embedded DB Inspector Module")
    r_45.bold = True
    r_45.font.size = Pt(11.5)
    r_45.font.color.rgb = RGBColor(142, 36, 170)

    p_45_b = doc.add_paragraph()
    p_45_b.add_run(
        "• Renders searchable transaction ledger tables with status indicators, risk scores, and receipt details.\n"
        "• Includes an in-app Database Inspector (db_viewer.py) allowing real-time audit of users, beneficiaries, transactions, and security event logs directly from the UI."
    )

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(10)

    # 05 FRONTEND WORKFLOW
    add_section_header(doc, "05", "FRONTEND WORKFLOW")
    p_wf = doc.add_paragraph()
    p_wf.paragraph_format.space_after = Pt(12)
    p_wf.add_run(
        "When a user opens the application, Streamlit initializes the session state and renders the responsive landing view. "
        "Unauthenticated users navigate the Two-Stage Registration Wizard where Clerk dispatches a 6-digit OTP code to verify their email address. "
        "Upon entering their password and 4-digit UPI PIN, account credentials are securely hashed with SHA-256 and stored in SQLite payguard_bank.db. "
        "When initiating a payment, the frontend sends transaction telemetry to FastAPI, receiving a PyTorch ML fraud risk score (0-100) and decision "
        "(ALLOW, VERIFY, REVIEW). If step-up authorization is required, the user validates their 4-digit UPI PIN before the transaction ledger updates, "
        "wallet balance adjusts, and the recipient is automatically saved to the frequent payees bar."
    ).font.color.rgb = RGBColor(51, 51, 51)

    # 06 CONCLUSION
    add_section_header(doc, "06", "CONCLUSION")
    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.space_after = Pt(12)
    p_conc.add_run(
        "The frontend system design delivers a robust, responsive, and secure user experience for PayGuard AI. By combining a zero-scroll "
        "Streamlit layout, Clerk OTP email authentication, SHA-256 pin isolation, dynamic SQLite payee persistence, and real-time PyTorch ML risk evaluation, "
        "the application ensures seamless digital wallet operation with industry-standard fraud prevention capabilities."
    ).font.color.rgb = RGBColor(51, 51, 51)

    # Footer line
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(20)
    r_ft = p_foot.add_run("WWW.VAMSCORE.COM   |   INNOVATE  |  DELIVER  |  GROW")
    r_ft.font.size = Pt(9.5)
    r_ft.font.bold = True
    r_ft.font.color.rgb = RGBColor(142, 36, 170)

    output_paths = [
        r"C:\Users\ASUS\.gemini\antigravity\scratch\payguard-ai\PayGuard_AI_Vamscore_Frontend_Project_Report_Clear.docx",
        r"C:\Users\ASUS\.gemini\antigravity\scratch\PayGuard_AI_Vamscore_Frontend_Project_Report_Clear.docx"
    ]
    for pth in output_paths:
        try:
            doc.save(pth)
            print(f"Successfully saved Vamscore Frontend Project Report at: {pth}")
        except PermissionError:
            print(f"Permission error for {pth}")

if __name__ == "__main__":
    build_vamscore_report()
