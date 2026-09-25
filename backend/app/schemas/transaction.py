"""
FastAPI Pydantic Schemas for Transaction Risk Analysis.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TransactionRequest(BaseModel):
    """Transaction request payload matching IEEE-CIS fraud detection feature schema."""
    transaction_id: int = Field(..., example=100185, description="Unique numeric transaction ID")
    user_id: str = Field(default="usr_8820", example="usr_8820", description="Customer identifier")
    amount: float = Field(..., gt=0.0, example=2500.0, description="Transaction monetary value in INR")
    timestamp: str = Field(..., example="2026-09-23T19:30:00+05:30", description="ISO 8601 transaction timestamp")
    product_cd: str = Field(default="W", example="W", description="Product code category")

    # Card & Account Features
    card1: Optional[int] = Field(default=1234, description="Card categorical feature 1")
    card2: Optional[int] = Field(default=567, description="Card categorical feature 2")
    card3: Optional[int] = Field(default=150, description="Card categorical feature 3")
    card4: Optional[str] = Field(default="visa", description="Card network type")
    card5: Optional[int] = Field(default=226, description="Card categorical feature 5")
    card6: Optional[str] = Field(default="debit", description="Card type (debit/credit)")

    # Location & Distance Features
    addr1: Optional[int] = Field(default=325, description="Billing region code")
    addr2: Optional[int] = Field(default=87, description="Billing country code")
    dist1: Optional[int] = Field(default=15, description="Distance metric 1")
    dist2: Optional[int] = Field(default=0, description="Distance metric 2")

    # Email Domains
    p_emaildomain: Optional[str] = Field(default="gmail.com", description="Purchaser email domain")
    r_emaildomain: Optional[str] = Field(default="example.com", description="Recipient email domain")

    # Device & Telemetry Signals
    device_type: Optional[str] = Field(default="mobile", description="Device type (mobile/desktop)")
    device_info: Optional[str] = Field(default="iOS Pro", description="Device details / browser agent")

    # Risk Indicators
    failed_attempts: Optional[int] = Field(default=0, description="Number of recent failed security attempts")
    is_new_device: Optional[bool] = Field(default=False, description="Whether device fingerprint is new")
    is_new_location: Optional[bool] = Field(default=False, description="Whether transaction location is new/VPN")
    high_velocity: Optional[bool] = Field(default=False, description="High velocity transfer sequence flag")
    recent_transactions: Optional[int] = Field(default=1, description="Transaction count in recent window")

    # Ledger Integrity Fields
    sender_debited: bool = Field(default=True, description="Whether sender account was debited")
    receiver_credited: bool = Field(default=True, description="Whether receiver account was credited")
    gateway_status: str = Field(default="SUCCESS", description="Gateway status code (SUCCESS/FAILED/TIMEOUT)")
    settlement_status: str = Field(default="COMPLETED", description="Settlement status")

class TransactionIntegrity(BaseModel):
    """Ledger state consistency assessment."""
    sender_debited: bool
    receiver_credited: bool
    gateway_status: str
    settlement_status: str
    is_consistent: bool
    inconsistency_reason: Optional[str] = None

class PredictionResponse(BaseModel):
    """Output risk evaluation schema produced by FastAPI RXT engine."""
    transaction_id: int
    fraud_probability: float = Field(..., ge=0.0, le=1.0, description="Raw RXT Neural Model fraud probability")
    risk_score: int = Field(..., ge=0, le=100, description="Composite Risk Score (0-100)")
    decision: str = Field(..., description="Decision tier: ALLOW, VERIFY, REVIEW")
    risk_signals: List[str] = Field(..., description="Human-readable security risk rationale list")
    transaction_integrity: TransactionIntegrity
    model_version: str = Field(default="RXT-ResNeXt-GRU-v1.2", description="ML model architecture version")
