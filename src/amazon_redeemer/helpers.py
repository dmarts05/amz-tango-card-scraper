"""Module containing helper functions for the amazon_redeemer module"""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.browser.extra_actions import wait_for_element

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

    from src.utils.schemas import AmazonCard


def get_amazon_sign_in_link(amazon_link: str) -> str:
    """
    Get the sign in link for the given amazon link

    Args:
        amazon_link: The amazon link to get the sign in link for

    Returns:
        The sign in link for the given amazon link
    """

    from .constants import SIGN_IN_LINK_TEMPLATE

    # Strip https and www from amazon_link
    amazon_link = amazon_link.replace("https://", "").replace("www.", "")
    sign_in_link = SIGN_IN_LINK_TEMPLATE.format(amazon_link, amazon_link)

    return sign_in_link


def sign_in_to_amazon(browser: WebDriver, email: str, password: str, otp: str, amazon_link: str) -> None:
    """
    Sign in to Amazon with the given credentials and OTP code

    Args:
        browser: The browser to use
        email: The email to sign in with
        password: The password to sign in with
        otp: The OTP code to sign in with
        amazon_link: The amazon link to sign in to

    Raises:
        ValueError: If the sign in process failed
    """

    from src.utils.otp import get_otp_code

    from .constants import (
        CONTINUE_BUTTON_ID,
        EMAIL_FIELD_ID,
        NAV_LOGO_ID,
        OTP_FIELD_ID,
        PASSWORD_FIELD_ID,
        SIGN_IN_BTN_1_ID,
        SIGN_IN_BTN_2_ID,
    )

    # Get sign in link
    sign_in_link = get_amazon_sign_in_link(amazon_link)

    # Get to sign in page
    browser.get(sign_in_link)

    # Write email
    print("[AMAZON SIGN IN] Writing email...")
    email_field = wait_for_element(browser, (By.ID, EMAIL_FIELD_ID))
    email_field.send_keys(email)  # type: ignore

    # Click continue
    continue_btn = browser.find_element(By.ID, CONTINUE_BUTTON_ID)
    continue_btn.click()

    # Write password
    print("[AMAZON SIGN IN] Writing password...")
    try:
        password_field = wait_for_element(browser, (By.ID, PASSWORD_FIELD_ID))
    except TimeoutException:
        # Malformed email in previous step
        raise ValueError("Malformed email")
    password_field.send_keys(password)  # type: ignore

    # Click sign in (before OTP)
    sign_in_btn_1 = browser.find_element(By.ID, SIGN_IN_BTN_1_ID)
    sign_in_btn_1.click()

    # Write OTP code
    print("[AMAZON SIGN IN] Writing OTP code...")
    otp_code = get_otp_code(otp)
    try:
        otp_field = wait_for_element(browser, (By.ID, OTP_FIELD_ID))
    except TimeoutException:
        # Malformed password in previous step
        raise ValueError("Malformed password")
    otp_field.send_keys(otp_code)  # type: ignore

    # Click sign in (after OTP)
    sign_in_btn_2 = browser.find_element(By.ID, SIGN_IN_BTN_2_ID)
    sign_in_btn_2.click()

    # Check if we have managed to successfully sign in
    # To do so, we need to check wether the nav-logo is present or not
    try:
        wait_for_element(browser, (By.ID, NAV_LOGO_ID), timeout=5)
    except TimeoutException:
        # Malformed OTP code in previous step
        raise ValueError("Malformed OTP code")


def redeem_amazon_gift_card(browser: WebDriver, amazon_card: AmazonCard) -> None:
    """
    Redeem the given amazon gift card

    Args:
        browser: The browser to use
        amazon_card: The amazon card to redeem
    """
    from .constants import (
        GIFT_CARD_CODE_FIELD_ID,
        REDEEM_BUTTON_ID,
        SUCCESSFUL_REDEEM_BOX_ID,
    )

    # Get to gift card redeem page
    browser.get(amazon_card.amazon_link + "/gc/redeem")

    # Write gift card code
    print(f"[AMAZON REDEEMER] Writing gift card code {amazon_card.redeem_code}...")
    gift_card_code_field = wait_for_element(browser, (By.ID, GIFT_CARD_CODE_FIELD_ID))
    gift_card_code_field.send_keys(amazon_card.redeem_code)  # type: ignore

    # Click redeem button
    print("[AMAZON REDEEMER] Redeeming code...")
    redeem_btn = browser.find_element(By.ID, REDEEM_BUTTON_ID)
    redeem_btn.click()

    # Check if code has been correctly redeemed
    try:
        wait_for_element(browser, (By.ID, SUCCESSFUL_REDEEM_BOX_ID), timeout=5)
    except TimeoutException:
        print("[AMAZON REDEEMER] Code couldn't be redeemed!")
        return

    print("[AMAZON REDEEMER] Code was successfully redeemed!")
    amazon_card.redeem_status = True
