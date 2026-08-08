import socket
import requests


def get_ip_information(domain: str):
    """
    Returns IP address and geolocation information.
    """

    try:
        # Resolve domain to IP
        ip = socket.gethostbyname(domain)

        # Query ip-api.com
        response = requests.get(
            f"http://ip-api.com/json/{ip}"
        ).json()

        return {
            "success": True,
            "ip": ip,
            "country": response.get("country"),
            "city": response.get("city"),
            "isp": response.get("isp"),
            "org": response.get("org"),
            "asn": response.get("as")
        }

    except Exception as e:

        return {
            "success": False,
            "reason": str(e)
        }