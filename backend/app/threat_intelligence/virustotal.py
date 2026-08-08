import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

URL = "https://www.virustotal.com/api/v3/urls"


def check_url_virustotal(url: str):
    """
    Checks a URL using VirusTotal.
    """

    if not API_KEY:
        return {
            "success": False,
            "reason": "VirusTotal API key not found."
        }

    try:
        # Step 1: Submit URL
        headers = {
            "x-apikey": API_KEY
        }

        response = requests.post(
            URL,
            headers=headers,
            data={"url": url}
        )

        if response.status_code != 200:
            return {
                "success": False,
                "reason": response.text
            }

        analysis_id = response.json()["data"]["id"]

        # Step 2: Fetch analysis report
        report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

        report = requests.get(
            report_url,
            headers=headers
        )

        if report.status_code != 200:
            return {
                "success": False,
                "reason": report.text
            }

        stats = report.json()["data"]["attributes"]["stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)

        return {
            "success": True,
            "malicious": malicious,
            "suspicious": suspicious,
            "harmless": harmless
        }

    except Exception as e:
        return {
            "success": False,
            "reason": str(e)
        }