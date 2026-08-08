def analyze_payload(payload: str):
    """
    Detect the type of data stored inside a QR code.
    """

    payload = payload.strip()

    if payload.startswith(("http://", "https://")):
        return {
            "type": "URL",
            "details": payload
        }

    elif payload.startswith("WIFI:"):
        return {
            "type": "WiFi",
            "details": payload
        }

    elif payload.startswith("BEGIN:VCARD"):
        return {
            "type": "vCard",
            "details": payload
        }

    elif payload.startswith("mailto:"):
        return {
            "type": "Email",
            "details": payload
        }

    elif payload.startswith("SMSTO:"):
        return {
            "type": "SMS",
            "details": payload
        }

    elif payload.startswith("tel:"):
        return {
            "type": "Phone",
            "details": payload
        }

    elif payload.startswith("geo:"):
        return {
            "type": "Location",
            "details": payload
        }

    elif payload.startswith("upi://"):
        return {
            "type": "UPI Payment",
            "details": payload
        }

    else:
        return {
            "type": "Plain Text",
            "details": payload
        }