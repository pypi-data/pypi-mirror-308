import dns.resolver
from dns.resolver import NoNameservers
from functools import lru_cache


@lru_cache(maxsize=10000)
def is_domain_valid(domain: str) -> bool:
    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        return bool(mx_records)
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        NoNameservers,
        dns.resolver.Timeout,
    ):
        return False
