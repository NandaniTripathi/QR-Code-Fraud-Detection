from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.utils.file_handler import save_uploaded_file
from backend.app.services.qr_decoder import decode_qr

from backend.app.security.url_features import extract_url_features
from backend.app.security.phishing_detector import detect_phishing
from backend.app.security.risk_score import calculate_risk_score

from backend.app.schemas.scan_response import ScanResponse

router = APIRouter(
    prefix="/scan",
    tags=["QR Scanner"]
)


@router.get("/")
def scan_info():
    return {
        "message": "QR Scanner API is ready."
    }


@router.post("/upload", response_model=ScanResponse)
async def upload_qr(file: UploadFile = File(...)):
    try:
        # Save uploaded image
        saved_path = save_uploaded_file(file)

        # Decode QR code
        decoded_url = decode_qr(saved_path)

        # Extract URL features
        features = extract_url_features(decoded_url)

        # Rule-based phishing detection
        phishing_result = detect_phishing(features)

        # Final risk assessment
        risk = calculate_risk_score(phishing_result)

        # Return response
        return ScanResponse(
            filename=file.filename,
            decoded_url=decoded_url,
            risk_score=risk["risk_score"],
            risk_level=risk["risk_level"],
            reasons=risk["reasons"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )