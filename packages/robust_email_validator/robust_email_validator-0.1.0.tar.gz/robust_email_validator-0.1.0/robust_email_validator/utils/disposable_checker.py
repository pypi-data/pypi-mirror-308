import requests
from robust_email_validator.config import DISPOSABLE_URL
from typing import Set

# Set to hold disposable domains
disposable_domains: Set[str] = set()


def load_disposable_domains() -> None:
    """Load disposable domains from an external source."""
    global disposable_domains
    try:
        response = requests.get(DISPOSABLE_URL)
        response.raise_for_status()
        disposable_domains = set(response.json())
    except requests.RequestException as e:
        print(f"Error fetching disposable domains: {e}")
    except ValueError as e:
        print(f"Error parsing disposable domains JSON: {e}")


def is_disposable(domain: str) -> bool:
    """Check if the domain is disposable by looking it up in the loaded set."""
    return domain.lower() in disposable_domains


def refresh_disposable_domains() -> None:
    """Refresh the disposable domain list."""
    load_disposable_domains()
