from robust_email_validator.services.email_validator import (
    validate_email,
    check_email_disposable,
    check_email_mx,
)


def test_validate_email():
    email = "test@example.com"
    result = validate_email(email)
    assert result.email == email
    assert result.is_valid is True


def test_check_email_disposable():
    email = "test1@00reviews.com"
    result = check_email_disposable(email)
    assert result.email == email
    assert result.is_valid is False


def test_check_email_mx():
    email = "test@example.com"
    result = check_email_mx(email)
    assert result.email == email
    assert result.is_valid is True
