# 🛡️ PAYGUARD AI
> **Intelligent Online Payment Fraud Detection — Digital Banking Security Sandbox**

PAYGUARD AI is a production-quality frontend prototype of a modern digital banking payment platform with embedded real-time AI payment fraud detection and ledger integrity monitoring.

---

## ⚡ Quick Start

Run the application locally with Streamlit:

```bash
cd payguard-ai
streamlit run frontend/streamlit_app.py
```

or simply:

```bash
streamlit run app.py
```

---

## 🚀 Product Features

1. **Banking Dashboard**
   - Live metrics: Available Balance (`₹85,420.00`), Today's Spending (`₹4,850.00`), Payments Count (`12`), Security Status (`Protected`).
   - Quick Action shortcuts: Send Money, Beneficiaries, Transaction History, Security Center.
   - Real-time transaction feed and active security status indicators.

2. **Send Money Flow (Interactive Wizard)**
   - **Step 01: Recipient** — Select dummy beneficiaries (Rahul Kumar, Priya Sharma, Arjun Mehta, Neha Gupta) or add custom recipients.
   - **Step 02: Amount** — Quick chip selector (`+₹500`, `+₹1,500`, `+₹5,000`, `+₹12,500`), purpose dropdown (Personal, Food, Shopping, Bills, Education, Other), and optional notes.
   - **Step 03: Review Payment** — Visual receipt overview and calculated post-payment balance (`₹82,920.00`).
   - **Step 04: Security Analysis** — Animated CSS scanning radar and 6-step validation checklist simulation.
   - **Step 05: Payment Results** — 4 deterministic outcomes:
     - 🟢 **SUCCESS (ALLOW)** — Low risk (`8.4%`), score (`8/100`), completed transfer.
     - 🟡 **VERIFICATION REQUIRED (VERIFY)** — Medium risk (`34.8%`), step-up 2FA OTP simulation.
     - 🔴 **PAYMENT ON HOLD (REVIEW)** — High risk (`78.4%`), VPN/New device signal flags, manual review appeal.
     - ⚠ **PAYMENT STATUS INCONSISTENCY (RECONCILE)** — Ledger discrepancy (Sender Debited ✓, Gateway ACK ✓, Receiver Credit Failed ✕) with interactive auto-reconciliation.

3. **Payment Security Check**
   - Live custom payload security scanner allowing test inputs for amount, device fingerprint, IP location (VPN), and failed PIN attempts.

4. **Transaction History & Detail Receipt**
   - Search by ID, recipient, or amount. Filter by status or purpose category.
   - Click any transaction to open a detailed receipt drawer with a minute-by-minute execution timeline and risk signals.

5. **Security Center & Telemetry**
   - Meter gauges for Account Security, Fraud Monitoring, Device Security, and Transaction Telemetry.
   - Audit event logs and non-technical security summaries.

6. **How PayGuard AI Works**
   - 6-step visual pipeline diagram (PAYMENT → SIGNALS → AI ANALYSIS → CHECKS → RISK SCORE → DECISION).
   - Non-technical decision guides (ALLOW / VERIFY / REVIEW).
   - Developer tab detailing the **RXT Architecture** (ResNeXt feature extractor + GRU sequence network).

---

## 🛠 Project Architecture

```
payguard-ai/
├── app.py                         # Root application launcher
├── frontend/
│   ├── streamlit_app.py           # Main Streamlit app entry point
│   ├── components/                # Reusable UI component modules
│   │   ├── dashboard.py           # Banking Dashboard
│   │   ├── payment_flow.py        # Send Money 5-step wizard
│   │   ├── security_check_live.py # Interactive Security Check tool
│   │   ├── transactions.py        # Transaction History & Receipt timeline
│   │   ├── security.py            # Security Center & How It Works
│   │   ├── cards.py               # Metric cards, status badges, risk gauges
│   │   └── navigation.py         # Sidebar branding & Demo preset selector
│   ├── services/
│   │   └── mock_transaction_service.py # Frontend state & service layer (# FUTURE BACKEND INTEGRATION)
│   ├── data/
│   │   └── mock_data.py           # Seed data and demo scenarios
│   └── styles/
│       └── theme.py               # Custom CSS (Dark navy, glassmorphism, radar animations)
└── README.md
```

---

## 🔒 Future Backend Integration

The service layer in `frontend/services/mock_transaction_service.py` is cleanly decoupled from UI components. To connect to a live FastAPI + RXT backend later, replace mock service functions with HTTP calls:

```python
# FUTURE BACKEND INTEGRATION POINT
# Replace analyze_payment() with:
# response = requests.post("http://localhost:8000/api/v1/fraud/analyze", json=payload)
```
