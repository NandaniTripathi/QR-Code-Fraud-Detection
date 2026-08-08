KNOWN_CLOUD_PROVIDERS = {
    "Cloudflare",
    "Amazon",
    "Amazon AWS",
    "Google",
    "Google LLC",
    "Microsoft",
    "Azure",
    "DigitalOcean",
    "OVH",
    "Hetzner",
    "Linode",
    "Vultr"
}


def detect_hosting_provider(org: str):

    if not org:
        return {
            "provider": "Unknown",
            "risk": "Unknown"
        }

    for provider in KNOWN_CLOUD_PROVIDERS:

        if provider.lower() in org.lower():

            return {
                "provider": provider,
                "risk": "Cloud Hosting Provider"
            }

    return {
        "provider": org,
        "risk": "Standard ISP"
    }