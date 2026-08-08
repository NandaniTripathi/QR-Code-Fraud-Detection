from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.utils.file_handler import save_uploaded_file
from backend.app.services.qr_decoder import decode_qr

from backend.app.security.url_features import extract_url_features
from backend.app.security.phishing_detector import detect_phishing
from backend.app.security.risk_score import calculate_risk_score

from backend.app.threat_intelligence.whois_lookup import get_domain_age
from backend.app.threat_intelligence.virustotal import check_url_virustotal

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
        # ----------------------------------------------------
        # Step 1: Save uploaded image
        # ----------------------------------------------------
        saved_path = save_uploaded_file(file)

        # ----------------------------------------------------
        # Step 2: Decode QR code
        # ----------------------------------------------------
        decoded_url = decode_qr(saved_path)

        # ----------------------------------------------------
        # Step 3: Extract URL features
        # ----------------------------------------------------
        features = extract_url_features(decoded_url)
        print("FEATURES:", features)

        # ----------------------------------------------------
        # Step 4: WHOIS Lookup
        # ----------------------------------------------------
        domain_info = get_domain_age(features["domain"])
        print("WHOIS:", domain_info)

        # ----------------------------------------------------
        # Step 5: VirusTotal Lookup
        # ----------------------------------------------------
        vt_result = check_url_virustotal(decoded_url)
        print("VirusTotal:", vt_result)

        # ----------------------------------------------------
        # Step 6: Rule-Based Detection
        # ----------------------------------------------------
        phishing_result = detect_phishing(features)
        print("PHISHING RESULT:", phishing_result)

        # ----------------------------------------------------
        # Step 7: Initial Risk Score
        # ----------------------------------------------------
        risk = calculate_risk_score(phishing_result)

        # ----------------------------------------------------
        # Step 8: WHOIS Scoring
        # ----------------------------------------------------
        if domain_info["success"]:

            age = domain_info["domain_age_days"]

            if age < 30:
                risk["risk_score"] += 35
                risk["reasons"].append(
                    "Domain is less than 30 days old."
                )

            elif age < 180:
                risk["risk_score"] += 20
                risk["reasons"].append(
                    "Domain is relatively new."
                )

        # ----------------------------------------------------
        # Step 9: VirusTotal Scoring
        # ----------------------------------------------------
        if vt_result["success"]:

            malicious = vt_result["malicious"]
            suspicious = vt_result["suspicious"]

            if malicious > 0:
                risk["risk_score"] += 50
                risk["reasons"].append(
                    f"VirusTotal detected {malicious} malicious vendors."
                )

            elif suspicious > 0:
                risk["risk_score"] += 25
                risk["reasons"].append(
                    f"VirusTotal detected {suspicious} suspicious vendors."
                )

        # ----------------------------------------------------
        # Step 10: Limit Score
        # ----------------------------------------------------
        risk["risk_score"] = min(risk["risk_score"], 100)

        # ----------------------------------------------------
        # Step 11: Recalculate Risk Level
        # ----------------------------------------------------
        if risk["risk_score"] >= 70:
            risk["risk_level"] = "High"
        elif risk["risk_score"] >= 40:
            risk["risk_level"] = "Medium"
        else:
            risk["risk_level"] = "Low"

        # ----------------------------------------------------
        # Step 12: Return Response
        # ----------------------------------------------------
        return ScanResponse(
            filename=file.filename,
            decoded_url=decoded_url,
            risk_score=risk["risk_score"],
            risk_level=risk["risk_level"],
            reasons=risk["reasons"],
            domain_age_days=(
                domain_info["domain_age_days"]
                if domain_info["success"]
                else None
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )