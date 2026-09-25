"""
FastAPI Main Application Entry Point.
Runs the PayGuard AI backend server exposing /api/v1/health and /api/v1/predict.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes import router

app = FastAPI(
    title="PayGuard AI Security Backend",
    description="Real-Time Payment Fraud Detection API using ResNeXt + GRU (RXT)",
    version="1.2.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Enable CORS for Streamlit / Frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API endpoints router
app.include_router(router)

@app.get("/", summary="Root Endpoint")
def read_root():
    return {
        "service": "PayGuard AI Security Backend",
        "status": "online",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
