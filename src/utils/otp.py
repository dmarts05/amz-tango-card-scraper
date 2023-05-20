"""Module for generating OTPs."""
from pyotp import TOTP


def get_otp_code(otp_key: str) -> str:
    """
    Generate OTP code from key.

    Args:
        otp_key: Key to generate OTP code.

    Returns:
        Generated OTP code.
    """
    return TOTP(otp_key.strip().replace(" ", "")).now()
