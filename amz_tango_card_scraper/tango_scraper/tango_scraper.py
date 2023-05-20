from __future__ import annotations

from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By

from amz_tango_card_scraper.browser.extra_actions import wait_for_element
from amz_tango_card_scraper.utils.schemas import AmazonCard

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

    from amz_tango_card_scraper.utils.schemas import TangoCard


def scrap_amazon_gift_cards(browser: WebDriver, tango_cards: List[TangoCard]) -> List[AmazonCard]:
    """
    Scrapes the amazon gift cards from the tango cards.

    Args:
        browser: the browser that will be used to scrape the amazon gift cards
        tango_cards: the tango cards that will be scraped

    Returns:
        The amazon gift cards that were scraped
    """
    from .constants import (
        AMZ_GIFT_CARD_CODE_WRAPPER_CSS_SELECTOR,
        HEADS_UP_CSS_SELECTOR,
        HEADS_UP_ERROR_CLASS,
        REDEEM_BUTTON_CSS_SELECTOR,
        SECURITY_CODE_ID,
    )

    amazon_cards: List[AmazonCard] = []
    for tc in tango_cards:
        # Go to the Tango card URL
        print(f"[TANGO SCRAPER] Going to {tc.tango_link}")

        browser.get(tc.tango_link)

        # Send security code to security code field (wait until it is visible)
        print("[TANGO SCRAPER] Sending security code to security code field...")
        security_code_field = wait_for_element(
            browser,
            (By.ID, SECURITY_CODE_ID),
        )
        security_code_field.send_keys(tc.security_code)  # type: ignore

        # Click redeem button
        print("[TANGO SCRAPER] Clicking redeem button...")
        redeem_button = browser.find_element(By.CSS_SELECTOR, REDEEM_BUTTON_CSS_SELECTOR)  # type: ignore
        redeem_button.click()

        # Check whether the security code was valid or not
        print("[TANGO SCRAPER] Checking whether the security code was valid...")
        heads_up = wait_for_element(
            browser,
            (By.CSS_SELECTOR, HEADS_UP_CSS_SELECTOR),
        )
        # Check whether the heads up message is a success or an error
        if HEADS_UP_ERROR_CLASS in heads_up.get_attribute("class"):  # type: ignore
            # Invalid security code
            print("[ERROR] Failed to redeem Tango Card")
            continue

        # Valid security code
        print("[TANGO SCRAPER] Tango Card successfully redeemed")

        # Wait for Amazon gift card code to be visible and get it
        redeem_code = (
            wait_for_element(  # type: ignore
                browser,
                (
                    By.CSS_SELECTOR,
                    AMZ_GIFT_CARD_CODE_WRAPPER_CSS_SELECTOR,
                ),
            )
            .find_element(By.XPATH, "./span")
            .text
        )  # type: ignore

        # Add Amazon gift card to list
        amazon_cards.append(AmazonCard(redeem_code=redeem_code, redeem_status=False, amazon_link=tc.amazon_link))

    return amazon_cards