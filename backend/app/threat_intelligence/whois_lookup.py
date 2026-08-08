import whois
from datetime import datetime, timezone


def get_domain_age(domain: str):
    """
    Returns WHOIS information for a domain.
    """

    try:
        info = whois.whois(domain)

        creation_date = info.creation_date

        # Some WHOIS servers return a list
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return {
                "success": False,
                "reason": "Creation date unavailable."
            }

        # Make both datetimes timezone-aware
        if creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        age_days = (now - creation_date).days

        return {
            "success": True,
            "creation_date": creation_date.strftime("%Y-%m-%d"),
            "domain_age_days": age_days
        }

    except Exception as e:
        return {
            "success": False,
            "reason": str(e)
        }