import pytest
from app.utils.otp import get_otp_code


def test_get_otp_code():
    # Test case 1: OTP code is valid
    otp_key = "PDGD NHNS BZU4 4USZ GBW5 YB7N 7VOQ TKTO 2HZI BCOZ U4JU FMNM MHKA"
    otp_code = get_otp_code(otp_key)
    assert isinstance(otp_code, str)
    assert len(otp_code) == 6
    assert otp_code.isdigit()

    # Test case 2: OTP code is invalid
    otp_key = "test invalid otp key"
    with pytest.raises(Exception):
        get_otp_code(otp_key)
