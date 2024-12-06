import re
from robust_email_validator.utils.dns_checker import is_domain_valid
from robust_email_validator.utils.disposable_checker import is_disposable
from robust_email_validator.schemas.email import EmailResponse


class EmailFormatError(Exception):
    """Raised when the email format is invalid."""


class DisposableEmailError(Exception):
    """Raised when the email domain is disposable."""


class EmailMXRecordError(Exception):
    """Raised when the email domain has no valid MX records."""


def check_email_pattern(email: str) -> bool:
    """Check if the email matches the correct pattern using regex."""
    return bool(
        re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email.strip())
    )


def validate_email(email: str) -> EmailResponse:
    """Validate the email pattern, disposable domain, and MX record, raising an error if validation fails."""

    if not check_email_pattern(email):
        raise EmailFormatError("Invalid email format.")
    domain = email.split("@")[-1]
    if is_disposable(domain):
        raise DisposableEmailError("Disposable email addresses are not allowed.")
    if not is_domain_valid(domain):
        raise EmailMXRecordError("Domain has no valid MX records.")
    return EmailResponse(email=email, is_valid=True, message="Email is valid.")


def check_email_disposable(email: str) -> EmailResponse:
    """Check if the email domain is disposable."""
    domain = email.split("@")[-1]
    disposable = is_disposable(domain)
    return EmailResponse(email=email, is_valid=disposable)


def check_email_mx(email: str) -> EmailResponse:
    """Check if the email domain has valid MX records."""
    domain = email.split("@")[-1]
    has_mx = is_domain_valid(domain)
    return EmailResponse(email=email, is_valid=has_mx)
