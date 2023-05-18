"""Module containing the main function of the program."""

import os

from app.browser import get_chrome_browser
from app.config_handler import get_config
from app.gmail_scraper import scrape_tango_cards
from app.tango_scraper import scrap_amazon_gift_cards


def main() -> None:
    # Get program configuration
    print("[INFO] Reading configuration file...")
    # Get path of config file in the parent directory
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
    config = get_config(file_path=config_file_path)
    print("[INFO] Configuration file read successfully")

    # Scrape Tango Cards from Gmail
    print("[INFO] Scraping Tango Cards from Gmail...")
    tango_cards = scrape_tango_cards(
        email=config.gmail.get("email", ""),
        app_password=config.gmail.get("app_password", ""),
        from_list=config.from_list,
        trash=config.script.get("trash", False),
    )
    print("[INFO] Tango Cards scraped successfully")

    # Get Selenium browser
    browser = get_chrome_browser(
        headless=config.script.get("headless", True),
        no_images=config.script.get("no_images", True),
        no_webdriver_manager=config.script.get("no_webdriver_manager", False),
    )

    # Scrape Amazon gift card codes from Tango Cards
    print("[INFO] Scraping Amazon gift card codes from Tango Cards...")
    amazon_cards = scrap_amazon_gift_cards(browser=browser, tango_cards=tango_cards)
    print("[INFO] Amazon gift card codes scraped successfully")

    # Print Amazon gift card codes
    amazon_cards_str = "\n".join([str(card) for card in amazon_cards])
    print(amazon_cards_str)

    # Close Selenium browser
    browser.quit()


if __name__ == "__main__":
    main()
