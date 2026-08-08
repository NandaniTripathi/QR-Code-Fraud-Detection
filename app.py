from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.app.utils.file_handler import save_uploaded_file
from backend.app.services.qr_decoder import decode_qr

from backend.app.security.payload_analyzer import analyze_payload
from backend.app.security.url_features import extract_url_features
from backend.app.security.phishing_detector import detect_phishing
from backend.app.security.risk_score import calculate_risk_score
from backend.app.security.hosting_provider import detect_hosting_provider
from dataset.models import create_tables
from dataset.operations import save_scan

from backend.app.threat_intelligence.whois_lookup import get_domain_age
from backend.app.threat_intelligence.virustotal import check_url_virustotal
from backend.app.threat_intelligence.ip_lookup import get_ip_information
from backend.app.threat_intelligence.file_scanner import (
    is_downloadable,
    scan_downloadable_file
)
app = Flask(__name__)
CORS(app)

create_tables()


@app.route("/")
def home():
    return jsonify({
        "message": "QR Shield API is running."
    })


@app.route("/scan", methods=["POST"])
def scan_qr():
    try:

        # -----------------------------
        # Check uploaded file
        # -----------------------------
        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded."
            }), 400

        file = request.files["file"]

        # -----------------------------
        # Save uploaded image
        # -----------------------------
        saved_path = save_uploaded_file(file)

        # -----------------------------
        # Decode QR Code
        # -----------------------------
        decoded_data = decode_qr(saved_path)

        # -----------------------------
        # Detect Payload Type
        # -----------------------------
        payload = analyze_payload(decoded_data)

        # =====================================================
        # DEFAULT VALUES
        # (Used for non-URL QR codes)
        # =====================================================

        risk = {
            "risk_score": 0,
            "risk_level": "Low",
            "reasons": []
        }

        domain_info = {
            "success": False
        }

        vt_result = {
            "success": False,
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0
        }

        file_scan = {
        "success": False,
        "reason": "Not applicable"
        }

        ip_info = {
            "success": False,
            "reason": "Not applicable"
        }

        hosting = {
            "provider": "Not applicable",
            "risk": "Not applicable"
        }

        # =====================================================
        # URL ANALYSIS
        # =====================================================

        if payload["type"] == "URL":

            # URL Features
            features = extract_url_features(decoded_data)

            # Rule-based phishing detection
            phishing_result = detect_phishing(features)

            # Initial Risk
            risk = calculate_risk_score(phishing_result)

            # WHOIS
            domain_info = get_domain_age(features["domain"])

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

            # VirusTotal
            vt_result = check_url_virustotal(decoded_data)

            # File Scan
            file_scan = {
                "success": False,
                "reason": "Not a downloadable file."
            }

            if is_downloadable(decoded_data):
                file_scan = scan_downloadable_file(decoded_data)

            if vt_result["success"]:

                if vt_result["malicious"] > 0:
                    risk["risk_score"] += 50
                    risk["reasons"].append(
                        f"VirusTotal detected {vt_result['malicious']} malicious vendors."
                    )

                elif vt_result["suspicious"] > 0:
                    risk["risk_score"] += 25
                    risk["reasons"].append(
                        f"VirusTotal detected {vt_result['suspicious']} suspicious vendors."
                    )

            # File Scan Scoring
            if file_scan["success"]:

                if file_scan["malicious"] > 0:

                    risk["risk_score"] += 60

                    risk["reasons"].append(
                        f"Downloaded file detected as malicious by {file_scan['malicious']} vendors."
                )

                elif file_scan["suspicious"] > 0:

                    risk["risk_score"] += 30

                    risk["reasons"].append(
                        f"Downloaded file detected as suspicious by {file_scan['suspicious']} vendors."
              )        

            # IP Geolocation
            ip_info = get_ip_information(features["domain"])

            # Hosting Provider
            if ip_info["success"]:
                hosting = detect_hosting_provider(ip_info["org"])

            # Limit score
            risk["risk_score"] = min(risk["risk_score"], 100)

            # Risk Level
            if risk["risk_score"] >= 70:
                risk["risk_level"] = "High"

            elif risk["risk_score"] >= 40:
                risk["risk_level"] = "Medium"

            else:
                risk["risk_level"] = "Low"

        # =====================================================
        # RESPONSE
        # =====================================================
        # Save scan to database
        save_scan(
            filename=file.filename,
            payload_type=payload["type"],
            decoded_url=decoded_data,
            risk_score=risk["risk_score"],
            risk_level=risk["risk_level"]
   )
        return jsonify({

            "filename": file.filename,

            "decoded_url": decoded_data,

            "payload_type": payload["type"],
            "payload_data": payload["details"],

            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "reasons": risk["reasons"],

            "domain_age_days": (
                domain_info["domain_age_days"]
                if domain_info["success"]
                else None
            ),

            "virustotal": vt_result,

            "ip_information": ip_info,

            "hosting_provider": hosting,

            "file_scan": file_scan

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)