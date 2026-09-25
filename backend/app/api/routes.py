"""
FastAPI Router exposing health and real-time fraud prediction endpoints.
"""

import datetime
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.transaction import TransactionRequest, PredictionResponse
from backend.app.services.predictor import RXTPredictor
from backend.app.services.risk_engine import RiskEngine

router = APIRouter(prefix="/api/v1", tags=["Payment Security API"])

predictor = RXTPredictor()
risk_engine = RiskEngine()

@router.get("/health", summary="System Health Status")
def health_check():
    """Returns backend system status and model readiness."""
    return {
        "status": "healthy",
        "service": "PayGuard AI Fraud Detection Engine",
        "model_version": "RXT-ResNeXt-GRU-v1.2",
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate Real-Time Transaction Risk"
)
def predict_fraud_risk(request: TransactionRequest):
    """
    Evaluates input transaction data through RXT model and risk engine,
    returning decision (ALLOW, VERIFY, REVIEW), risk score, signals, and integrity metrics.
    """
    try:
        data = request.model_dump()
        fraud_prob = predictor.predict(data)
        eval_result = risk_engine.evaluate(data, fraud_prob)

        response_payload = {
            "transaction_id": request.transaction_id,
            "fraud_probability": eval_result["fraud_probability"],
            "risk_score": eval_result["risk_score"],
            "decision": eval_result["decision"],
            "risk_signals": eval_result["risk_signals"],
            "transaction_integrity": eval_result["transaction_integrity"],
            "model_version": "RXT-ResNeXt-GRU-v1.2"
        }
        return response_payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Security engine error: {str(exc)}"
        ) from exc
