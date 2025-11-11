import secrets


def generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP of given length using a cryptographically secure generator."""
    digits = "0123456789"
    return ''.join(secrets.choice(digits) for _ in range(length))
