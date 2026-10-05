"""
PayGuard AI - Frontend Configuration Module.
Provides central configuration settings and backend API base URL with environment variable support.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend API Endpoint Base URL (Default: http://127.0.0.1:8000)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# API Timeout Settings (in seconds)
API_HEALTH_TIMEOUT = int(os.getenv("API_HEALTH_TIMEOUT", "3"))
API_PREDICT_TIMEOUT = int(os.getenv("API_PREDICT_TIMEOUT", "10"))

# Default User Context for Sandbox Session
DEFAULT_USER_ID = "usr_8820"
