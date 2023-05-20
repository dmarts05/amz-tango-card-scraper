"""Module for redeeming Amazon gift cards."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.utils.schemas import AmazonCard

from .helpers import redeem_amazon_gift_card, sign_in_to_amazon

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


def redeem_amazon_gift_cards(
    browser: WebDriver, amazon_cards: List[AmazonCard], email: str, password: str, otp: str
) -> None:
    """
    Redeems the amazon gift cards.

    Args:
        browser: the browser that will be used to redeem the amazon gift cards
        amazon_cards: the amazon gift cards that will be redeemed
        email: the email that will be used to sign in to Amazon
        password: the password that will be used to sign in to Amazon
        otp: the otp key that will be used to sign in to Amazon

    Raises:
        ValueError: If the amazon gift cards are from different geographical regions or if the sign in process failed
    """
    # Check that every amazon link comes from the same geographical region
    if len(set([ac.amazon_link for ac in amazon_cards])) > 1:
        raise ValueError("All Amazon links must come from the same geographical region")

    # Sign in to Amazon
    sign_in_to_amazon(browser, email, password, otp, amazon_cards[0].amazon_link)

    # Redeem Amazon gift cards
    for ac in amazon_cards:
        redeem_amazon_gift_card(browser, ac)
