from typing import List

from browser.browser_extra_actions import wait_for_element
from schemas import AmazonCard, TangoCard
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def scrap_amazon_gift_cards(
    browser: WebDriver, tango_cards: List[TangoCard]
) -> List[AmazonCard]:
    """
    Scrapes the amazon gift cards from the tango cards.

    Args:
        browser: the browser that will be used to scrape the amazon gift cards
        tango_cards: the tango cards that will be scraped

    Returns:
        The amazon gift cards that were scraped
    """

    amazon_cards: List[AmazonCard] = []
    for tc in tango_cards:
        # Go to the Tango card URL
        print(f"[TANGO SCRAPER] Going to {tc.tango_link}")
        browser.get(tc.tango_link)

        # Send security code to security code field (wait until it is visible)
        print(
            "[TANGO SCRAPER] Sending security code to security code field..."
        )
        security_code_field = wait_for_element(
            browser=browser,
            locator=(By.ID, "input-47"),
        )
        security_code_field.send_keys(tc.security_code)  # type: ignore

        # Click redeem button
        print("[TANGO SCRAPER] Clicking redeem button...")
        redeem_button = browser.find_element(  # type: ignore
            By.CSS_SELECTOR, 'button[data-test-id="activateRewardButton"]'
        )
        redeem_button.click()

        # Check whether the security code was valid or not
        print(
            "[TANGO SCRAPER] Checking whether the security code was valid..."
        )
        heads_up = wait_for_element(
            browser=browser,
            locator=(By.CSS_SELECTOR, ".v-snack__wrapper"),
        )
        # Check whether the heads up message is a success or an error
        if "error" in heads_up.get_attribute("class"):  # type: ignore
            # Invalid security code
            print("[ERROR] Failed to redeem Tango Card")
            continue

        # Valid security code
        print("[TANGO SCRAPER] Tango Card successfully redeemed")

        # Wait for Amazon gift card code to be visible and get it
        redeem_code = (
            wait_for_element(  # type: ignore
                browser=browser,
                locator=(
                    By.CSS_SELECTOR,
                    'div[data-test-id="rewardCredentialValue-cardNumber"]',
                ),
            )
            .find_element(By.XPATH, "./span")
            .text
        )  # type: ignore

        # Add Amazon gift card to list
        amazon_cards.append(
            AmazonCard(redeem_code=redeem_code, amazon_link=tc.amazon_link)
        )

    return amazon_cards
