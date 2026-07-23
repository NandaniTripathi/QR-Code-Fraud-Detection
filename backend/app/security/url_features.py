from urllib.parse import urlparse
import ipaddress


def extract_url_features(url: str) -> dict:
    """
    Extract basic security-related features from a URL.
    """

    parsed = urlparse(url)

    domain = parsed.netloc

    try:
        ipaddress.ip_address(domain)
        has_ip = True
    except ValueError:
        has_ip = False

    features = {
        "url": url,
        "domain": domain,
        "scheme": parsed.scheme,
        "uses_https": parsed.scheme.lower() == "https",
        "url_length": len(url),
        "num_dots": domain.count("."),
        "has_ip_address": has_ip,
        "path_length": len(parsed.path)
    }

    return features