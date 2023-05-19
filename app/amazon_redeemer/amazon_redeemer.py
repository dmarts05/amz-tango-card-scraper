"""Module for redeeming Amazon gift cards."""

from typing import TYPE_CHECKING, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

    from app.utils.schemas import AmazonCard


def get_amazon_sign_in_link(amazon_link: str) -> str:
    # Strip https and www from amazon_link
    amazon_link = amazon_link.replace("https://", "").replace("www.", "")
    sign_in_link = f"https://www.{amazon_link}/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.{amazon_link}%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"  # noqa: E501

    return sign_in_link


def sign_in_to_amazon(browser: "WebDriver", email: str, password: str, otp: str, amazon_link: str) -> bool:
    from app.browser.extra_actions import wait_for_element
    from app.utils.otp import get_otp_code

    # Get sign in link
    sign_in_link = get_amazon_sign_in_link(amazon_link)

    # Get to sign in page
    browser.get(sign_in_link)

    # Write email
    print("[AMAZON SIGN IN] Writing email...")
    email_field = wait_for_element(browser, (By.ID, "ap_email"))
    email_field.send_keys(email)  # type: ignore

    # Click continue
    continue_btn = browser.find_element(By.ID, "continue")
    continue_btn.click()

    # Write password
    print("[AMAZON SIGN IN] Writing password...")
    try:
        password_field = wait_for_element(browser, (By.ID, "ap_password"))
    except TimeoutException:
        # Malformed email in previous step
        print("[ERROR] Failed to sign in to Amazon. Malformed email")
        return False

    password_field.send_keys(password)  # type: ignore

    # Click sign in (before OTP)
    sign_in_btn_1 = browser.find_element(By.ID, "signInSubmit")
    sign_in_btn_1.click()

    # Write OTP code
    print("[AMAZON SIGN IN] Writing OTP code...")
    otp_code = get_otp_code(otp)
    try:
        otp_field = wait_for_element(browser, (By.ID, "auth-mfa-otpcode"))
    except TimeoutException:
        # Malformed password in previous step
        print("[ERROR] Failed to sign in to Amazon. Malformed password")
        return False
    otp_field.send_keys(otp_code)  # type: ignore

    # Click sign in (after OTP)
    sign_in_btn_2 = browser.find_element(By.ID, "auth-signin-button")
    sign_in_btn_2.click()

    # Check if we have managed to successfully sign in
    # To do so, we need to check wether the nav-logo is present or not
    try:
        wait_for_element(browser, (By.ID, "nav-logo"))
    except TimeoutException:
        # Malformed OTP code in previous step
        print("[ERROR] Failed to sign in to Amazon. Malformed OTP code")
        return False

    return True


def redeem_amazon_gift_cards(
    browser: "WebDriver", amazon_cards: List["AmazonCard"], email: str, password: str, otp: str
) -> None:
    # Check that every amazon link comes from the same geographical region
    if len(set([ac.amazon_link for ac in amazon_cards])) > 1:
        raise ValueError("All Amazon links must come from the same geographical region")

    # Sign in to Amazon
    if not sign_in_to_amazon(browser, email, password, otp, amazon_cards[0].amazon_link):
        return

    pass
