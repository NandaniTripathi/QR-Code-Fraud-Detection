import hashlib
import os
import requests


def calculate_sha256(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def is_downloadable(url):

    extensions = (
        ".exe",
        ".apk",
        ".pdf",
        ".zip",
        ".rar",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx"
    )

    return url.lower().endswith(extensions)

import tempfile


def download_file(url):
    """
    Download a file temporarily and return its local path.
    """

    response = requests.get(url, timeout=15)

    response.raise_for_status()

    suffix = os.path.splitext(url)[1]

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    temp.write(response.content)

    temp.close()

    return temp.name

import os
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

def check_file_hash(hash_value):
    """
    Query VirusTotal using a SHA-256 hash.
    """

    if not VT_API_KEY:
        return {
            "success": False,
            "reason": "VirusTotal API key not found."
        }

    headers = {
        "x-apikey": VT_API_KEY
    }

    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {
            "success": False,
            "reason": "Hash not found."
        }

    data = response.json()["data"]["attributes"]["last_analysis_stats"]

    return {
        "success": True,
        "malicious": data["malicious"],
        "suspicious": data["suspicious"],
        "harmless": data["harmless"]
    }

def scan_downloadable_file(url):
    """
    Download a file, hash it, and check the hash on VirusTotal.
    """

    try:

        filepath = download_file(url)

        sha256 = calculate_sha256(filepath)

        result = check_file_hash(sha256)

        os.remove(filepath)

        return result

    except Exception as e:

        return {
            "success": False,
            "reason": str(e)
        }