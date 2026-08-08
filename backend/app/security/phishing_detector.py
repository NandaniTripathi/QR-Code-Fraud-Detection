from backend.app.core.security_rules import (
    SHORTENERS,
    SUSPICIOUS_KEYWORDS,
    SUSPICIOUS_TLDS
)


def detect_phishing(features: dict) -> dict:
    """
    Perform rule-based phishing detection.
    """

    reasons = []
    score = 0

    domain = features["domain"].lower()
    url = features["url"].lower()

    print("Domain:", domain)
    print("SHORTENERS:", SHORTENERS)
    print("Match:", domain in SHORTENERS)

    # Rule 1: HTTPS
    if not features["uses_https"]:
        score += 25
        reasons.append("Website does not use HTTPS.")

    # Rule 2: IP Address
    if features["has_ip_address"]:
        score += 35
        reasons.append("URL uses an IP address.")

    # Rule 3: Long URL
    if features["url_length"] > 75:
        score += 15
        reasons.append("URL is unusually long.")

    # Rule 4: Too many subdomains
    if features["num_dots"] > 3:
        score += 15
        reasons.append("Too many subdomains.")

    # Rule 5: Long path
    if features["path_length"] > 30:
        score += 10
        reasons.append("Long URL path.")

    # Rule 6: URL shortener
    if domain in SHORTENERS:
        score += 25
        reasons.append("URL uses a shortening service.")

    # Rule 7: Suspicious keywords
    found_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url:
            found_keywords.append(keyword)

    if found_keywords:
        score += 20
        reasons.append(
            "Suspicious keywords detected: "
            + ", ".join(found_keywords)
        )

    # Rule 8: Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 15
            reasons.append(f"Suspicious domain extension ({tld}).")
            break

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