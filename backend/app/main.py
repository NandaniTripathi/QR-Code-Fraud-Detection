from fastapi import FastAPI
from backend.app.api.v1.scan import router as scan_router

app = FastAPI(
    title="QR Code Fraud Detection API",
    description="Backend API for detecting fraudulent QR codes",
    version="1.0.0"
)

app.include_router(scan_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the QR Code Fraud Detection API"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }