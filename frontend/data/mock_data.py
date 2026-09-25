"""
PayGuard AI - Mock Data Store.
Contains demo users, seed balances, and initial transaction history strictly as specified.
"""

from typing import Dict, List, Any

# Pre-configured demo users
DEMO_USERS: Dict[str, Dict[str, Any]] = {
    "9876543210": {
        "user_id": "usr_rahul",
        "name": "Rahul Kumar",
        "mobile": "9876543210",
        "pin": "1234",
        "upi_id": "rahul.k@payguard",
        "account_num": "ACC-8921-4409-7712",
        "initial_balance": 45250.00,
        "avatar_initials": "RK"
    },
    "9123456780": {
        "user_id": "usr_ananya",
        "name": "Ananya Sharma",
        "mobile": "9123456780",
        "pin": "5678",
        "upi_id": "ananya.s@payguard",
        "account_num": "ACC-3190-8821-9943",
        "initial_balance": 68500.00,
        "avatar_initials": "AS"
    }
}

# Frequent Payees for quick selection in Send Money
SEED_FREQUENT_PAYEES: List[Dict[str, str]] = [
    {
        "name": "Priya Sharma",
        "identifier": "priya.s@upi",
        "type": "UPI ID",
        "avatar": "PS"
    },
    {
        "name": "Arjun Mehta",
        "identifier": "9820012345",
        "type": "Mobile",
        "avatar": "AM"
    },
    {
        "name": "Fresh Mart Grocery",
        "identifier": "merchant.freshmart@icici",
        "type": "Merchant UPI",
        "avatar": "FM"
    },
    {
        "name": "Cloud Kitchen Ltd",
        "identifier": "ACC-5521-0021-9912",
        "type": "Bank Account",
        "avatar": "CK"
    }
]

# Initial Seed Transaction History for Rahul Kumar
SEED_TRANSACTIONS: List[Dict[str, Any]] = [
    {
        "transaction_id": 1727248100001,
        "user_id": "usr_rahul",
        "recipient": "Fresh Mart Grocery",
        "recipient_id": "merchant.freshmart@icici",
        "amount": 1420.00,
        "timestamp": "2026-09-25T09:15:00+05:30",
        "date_group": "Today",
        "decision": "ALLOW",
        "status": "Completed",
        "risk_score": 8,
        "fraud_probability": 0.04,
        "risk_signals": [
            "Recognized billing merchant",
            "Consistent payment location",
            "Normal debit sequence"
        ],
        "transaction_integrity": {
            "is_consistent": True,
            "sender_debited": True,
            "receiver_credited": True,
            "gateway_status": "SUCCESS",
            "settlement_status": "COMPLETED"
        },
        "model_version": "RXT-ResNeXt-GRU-v1.2"
    },
    {
        "transaction_id": 1727161700002,
        "user_id": "usr_rahul",
        "recipient": "Priya Sharma",
        "recipient_id": "priya.s@upi",
        "amount": 2500.00,
        "timestamp": "2026-09-24T18:40:00+05:30",
        "date_group": "Yesterday",
        "decision": "ALLOW",
        "status": "Completed",
        "risk_score": 12,
        "fraud_probability": 0.08,
        "risk_signals": [
            "Frequent contact beneficiary",
            "Matched user device fingerprint"
        ],
        "transaction_integrity": {
            "is_consistent": True,
            "sender_debited": True,
            "receiver_credited": True,
            "gateway_status": "SUCCESS",
            "settlement_status": "COMPLETED"
        },
        "model_version": "RXT-ResNeXt-GRU-v1.2"
    },
    {
        "transaction_id": 1727075300003,
        "user_id": "usr_rahul",
        "recipient": "Unknown Merchant X",
        "recipient_id": "pay-terminal-991@temp.net",
        "amount": 18500.00,
        "timestamp": "2026-09-23T23:15:00+05:30",
        "date_group": "Earlier this week",
        "decision": "REVIEW",
        "status": "Security Review Blocked",
        "risk_score": 89,
        "fraud_probability": 0.86,
        "risk_signals": [
            "Unusual transaction amount for time window",
            "Unrecognized recipient domain",
            "High velocity transaction burst"
        ],
        "transaction_integrity": {
            "is_consistent": False,
            "sender_debited": False,
            "receiver_credited": False,
            "gateway_status": "BLOCKED",
            "settlement_status": "REJECTED",
            "inconsistency_reason": "Payment halted by real-time risk decision engine"
        },
        "model_version": "RXT-ResNeXt-GRU-v1.2"
    },
    {
        "transaction_id": 1726988900004,
        "user_id": "usr_rahul",
        "recipient": "Arjun Mehta",
        "recipient_id": "9820012345",
        "amount": 4200.00,
        "timestamp": "2026-09-22T14:10:00+05:30",
        "date_group": "Earlier this week",
        "decision": "VERIFY",
        "status": "Verified & Completed",
        "risk_score": 48,
        "fraud_probability": 0.35,
        "risk_signals": [
            "New IP address subnet detected",
            "Two-step verification step confirmed"
        ],
        "transaction_integrity": {
            "is_consistent": True,
            "sender_debited": True,
            "receiver_credited": True,
            "gateway_status": "SUCCESS",
            "settlement_status": "COMPLETED"
        },
        "model_version": "RXT-ResNeXt-GRU-v1.2"
    }
]
