"""Module for redeeming Amazon gift cards."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

from amz_tango_card_scraper.utils.schemas import AmazonCard

from .helpers import redeem_amazon_gift_card, sign_in_to_amazon, get_amazon_balance

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


def redeem_amazon_gift_cards(
    browser: WebDriver, amazon_cards: List[AmazonCard], email: str, password: str, otp: str
) -> Tuple[str, str]:
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

    Returns:
        A tuple containing the previous balance and the current balance
    """
    # Check that every amazon link comes from the same geographical region
    if len(set([ac.amazon_link for ac in amazon_cards])) > 1:
        raise ValueError("All Amazon links must come from the same geographical region")

    # Sign in to Amazon
    sign_in_to_amazon(browser, email, password, otp, amazon_cards[0].amazon_link)

    # Get balance prior to redeeming
    prev_balance = get_amazon_balance(browser, amazon_cards[0].amazon_link)

    # Redeem Amazon gift cards
    for ac in amazon_cards:
        redeem_amazon_gift_card(browser, ac)

    # Get balance after redeeming
    balance = get_amazon_balance(browser, amazon_cards[0].amazon_link)

    return (prev_balance, balance)
