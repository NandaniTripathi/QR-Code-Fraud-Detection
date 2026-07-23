def calculate_risk_score(rule_result: dict) -> dict:
    """
    Prepare the final risk assessment.

    Later this function will combine:
    - Rule-based score
    - Machine Learning score
    - Threat intelligence APIs
    """

    return {
        "risk_score": rule_result["risk_score"],
        "risk_level": rule_result["risk_level"],
        "reasons": rule_result["reasons"]
    }