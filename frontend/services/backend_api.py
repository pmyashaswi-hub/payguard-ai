"""
PayGuard AI - Backend API Integration Service & Contract Adapters.
Source of truth for communication with the FastAPI Risk Engine.
"""

import time
import datetime
from typing import Dict, Any, Tuple, Optional
import requests
import streamlit as st
from frontend.config import BACKEND_URL, API_HEALTH_TIMEOUT, API_PREDICT_TIMEOUT

class BackendAPIService:
    """Manages HTTP requests to FastAPI with single request and response adapters."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def build_transaction_payload(
        transaction_id: int,
        user_id: str,
        amount: float,
        timestamp: Optional[str] = None,
        product_cd: str = "W",
        card1: int = 1234,
        card2: int = 567,
        card3: int = 150,
        card4: str = "visa",
        card5: int = 226,
        card6: str = "debit",
        addr1: int = 325,
        addr2: int = 87,
        dist1: int = 15,
        dist2: int = 0,
        p_emaildomain: str = "gmail.com",
        r_emaildomain: str = "example.com",
        device_type: str = "mobile",
        device_info: str = "iOS Pro",
        failed_attempts: int = 0,
        is_new_device: bool = False,
        is_new_location: bool = False,
        high_velocity: bool = False,
        sender_debited: bool = True,
        receiver_credited: bool = True,
        gateway_status: str = "SUCCESS",
        settlement_status: str = "COMPLETED"
    ) -> Dict[str, Any]:
        """
        Adapter 1: Builds the exact canonical transaction request payload.
        Ensures recent_transactions is ALWAYS [] as specified by backend contract.
        """
        if timestamp is None:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
            timestamp = now.isoformat(timespec="seconds")

        payload = {
            "transaction_id": int(transaction_id),
            "user_id": str(user_id),
            "amount": float(amount),
            "timestamp": str(timestamp),
            "product_cd": str(product_cd),
            "card1": int(card1),
            "card2": int(card2),
            "card3": int(card3),
            "card4": str(card4),
            "card5": int(card5),
            "card6": str(card6),
            "addr1": int(addr1),
            "addr2": int(addr2),
            "dist1": int(dist1),
            "dist2": int(dist2),
            "p_emaildomain": str(p_emaildomain),
            "r_emaildomain": str(r_emaildomain),
            "device_type": str(device_type),
            "device_info": str(device_info),
            "failed_attempts": int(failed_attempts),
            "is_new_device": bool(is_new_device),
            "is_new_location": bool(is_new_location),
            "high_velocity": bool(high_velocity),
            "recent_transactions": [],  # Canonical spec: ALWAYS [], NEVER 0 or null
            "sender_debited": bool(sender_debited),
            "receiver_credited": bool(receiver_credited),
            "gateway_status": str(gateway_status),
            "settlement_status": str(settlement_status)
        }
        return payload

    @staticmethod
    def parse_prediction_response(response_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapter 2: Parses raw FastAPI response into verified domain model.
        NEVER re-derives or overrides risk scores or decisions.
        """
        integrity = response_json.get("transaction_integrity", {})
        is_consistent = integrity.get("is_consistent", True)
        
        # Check if ledger integrity requires reconciliation
        reconciliation_required = (not is_consistent) or (
            integrity.get("gateway_status") == "SUCCESS" and not integrity.get("receiver_credited")
        )

        return {
            "transaction_id": response_json.get("transaction_id"),
            "fraud_probability": float(response_json.get("fraud_probability", 0.0)),
            "risk_score": int(response_json.get("risk_score", 0)),
            "decision": str(response_json.get("decision", "ALLOW")).upper(),
            "risk_signals": list(response_json.get("risk_signals", [])),
            "transaction_integrity": integrity,
            "reconciliation_required": reconciliation_required,
            "model_version": str(response_json.get("model_version", "RXT-ResNeXt-GRU-v1.2")),
            "raw_response": response_json
        }

    def check_health(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Queries GET /api/v1/health. Cached in session_state, checked once per session
        unless force_refresh is True.
        """
        if not force_refresh and "backend_health_status" in st.session_state:
            return st.session_state.backend_health_status

        endpoint = f"{self.base_url}/api/v1/health"
        try:
            resp = requests.get(endpoint, timeout=API_HEALTH_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                result = {
                    "is_connected": True,
                    "status_label": "Connected",
                    "service": data.get("service", "PayGuard AI Fraud Detection Engine"),
                    "model_version": data.get("model_version", "RXT-ResNeXt-GRU-v1.2"),
                    "checked_at": time.strftime("%H:%M:%S")
                }
            else:
                result = {
                    "is_connected": False,
                    "status_label": "Error",
                    "service": "Unavailable",
                    "model_version": "N/A",
                    "checked_at": time.strftime("%H:%M:%S")
                }
        except Exception:
            result = {
                "is_connected": False,
                "status_label": "Offline",
                "service": "FastAPI Unreachable",
                "model_version": "N/A",
                "checked_at": time.strftime("%H:%M:%S")
            }

        st.session_state.backend_health_status = result
        return result

    def predict_risk(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Sends POST /api/v1/predict.
        Handles network errors, timeouts, and schema compatibility transparently.
        Returns: (success_bool, parsed_response_or_None, friendly_error_message_or_None)
        """
        endpoint = f"{self.base_url}/api/v1/predict"
        
        # Schema Mismatch Resolution:
        # The frontend contract specifies 'recent_transactions' as [].
        # In the existing FastAPI backend schema, recent_transactions expects an integer count.
        # We prepare network_payload to safely send len(recent_transactions) if the backend requires an integer,
        # ensuring 0 crashes and complete backwards-compatibility.
        network_payload = dict(payload)
        if isinstance(network_payload.get("recent_transactions"), list):
            network_payload["recent_transactions"] = len(network_payload["recent_transactions"])

        try:
            response = requests.post(endpoint, json=network_payload, timeout=API_PREDICT_TIMEOUT)
            
            if response.status_code == 200:
                parsed = self.parse_prediction_response(response.json())
                return True, parsed, None
            
            elif response.status_code == 422:
                # Validation error
                return False, None, "Security engine rejected transaction payload format (422)."
            
            else:
                return False, None, f"Security service responded with status {response.status_code}."

        except requests.exceptions.Timeout:
            return False, None, "Security analysis request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return False, None, "Security analysis is currently unavailable. Please verify the backend service is running."
        except Exception as e:
            return False, None, "Unable to complete security analysis at this time."
