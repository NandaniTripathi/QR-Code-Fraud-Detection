def detect_phishing(features: dict) -> dict:
    """
    Perform rule-based phishing detection.
    """

    reasons = []
    score = 0

    # Rule 1
    if not features["uses_https"]:
        score += 25
        reasons.append("Website does not use HTTPS.")

    # Rule 2
    if features["has_ip_address"]:
        score += 35
        reasons.append("URL uses an IP address.")

    # Rule 3
    if features["url_length"] > 75:
        score += 15
        reasons.append("URL is unusually long.")

    # Rule 4
    if features["num_dots"] > 3:
        score += 15
        reasons.append("Too many subdomains.")

    # Rule 5
    if features["path_length"] > 30:
        score += 10
        reasons.append("Long URL path.")

    score = min(score, 100)

    if score >= 70:
        level = "High"

    elif score >= 40:
        level = "Medium"

    else:
        level = "Low"

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons
    }