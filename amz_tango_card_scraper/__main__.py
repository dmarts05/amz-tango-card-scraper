"""Module containing the main function of the program."""

import os

from requests.exceptions import RequestException

from amz_tango_card_scraper.amazon_redeemer.amazon_redeemer import (
    redeem_amazon_gift_cards,
)
from amz_tango_card_scraper.browser.chrome import get_chrome_browser
from amz_tango_card_scraper.config_parser.config_parser import parse_config
from amz_tango_card_scraper.gmail_scraper.gmail_scraper import scrape_tango_cards
from amz_tango_card_scraper.message.message_builder import (
    build_amazon_cards_message,
    build_tango_cards_message,
)
from amz_tango_card_scraper.message.message_sender import send_message_to_telegram
from amz_tango_card_scraper.message.message_storage import store_message
from amz_tango_card_scraper.tango_scraper.tango_scraper import scrap_amazon_gift_cards
from amz_tango_card_scraper.utils.logger import reset_log_file, setup_logger

logger = setup_logger(logger_name=__name__)


def main() -> None:
    # Reset log file
    reset_log_file()

    # **************************************************************
    # Show welcome message
    # **************************************************************
    logger.info("***********************************************")
    logger.info("*                                             *")
    logger.info("*          Amazon Tango Card Scraper          *")
    logger.info("*                                             *")
    logger.info("***********************************************")

    # **************************************************************
    # Get program configuration
    # **************************************************************
    logger.info("Reading configuration file...")
    # Get path of config file in the parent directory
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
    try:
        # Read config file
        config = parse_config(config_file_path)
    except ValueError as e:
        logger.error(str(e))
        exit(1)
    except FileNotFoundError:
        logger.error('Configuration file "config.yml" not found')
        exit(1)
    logger.info("Configuration file read successfully")
    logger.debug(f"Configuration: {config}")

    # **************************************************************
    # Scrape Tango Cards from Gmail
    # **************************************************************
    logger.info("Scraping Tango Cards from Gmail...")
    tango_cards = scrape_tango_cards(
        email=config.gmail.get("email", ""),
        app_password=config.gmail.get("app_password", ""),
        from_list=config.from_list,
        trash=config.script.get("trash", False),
    )
    logger.debug(f"Tango Cards: {tango_cards}")
    if not tango_cards:
        logger.info("No Tango Cards found, exiting...")
        exit(0)
    logger.info("Tango Cards scraped successfully")

    # **************************************************************
    # Get Selenium browser
    # **************************************************************
    browser = get_chrome_browser(
        headless=config.script.get("headless", True),
        no_images=config.script.get("no_images", True),
        no_webdriver_manager=config.script.get("no_webdriver_manager", False),
    )

    # **************************************************************
    # Scrape Amazon gift card codes from Tango Cards
    # **************************************************************
    logger.info("Scraping Amazon gift card codes from Tango Cards...")
    amazon_cards = scrap_amazon_gift_cards(browser=browser, tango_cards=tango_cards)
    logger.info("Finished scraping Amazon gift card codes from Tango Cards")
    logger.debug(f"Amazon gift card codes: {amazon_cards}")

    # **************************************************************
    # Attempt to redeem Amazon gift card codes if enabled
    # **************************************************************
    if config.script.get("redeem_amz", False):
        logger.info("Attempting to redeem Amazon gift card codes...")
        try:
            redeem_amazon_gift_cards(
                browser=browser,
                amazon_cards=amazon_cards,
                email=config.amazon.get("email", ""),
                password=config.amazon.get("password", ""),
                otp=config.amazon.get("otp", ""),
            )
            logger.info("Finished redeeming Amazon gift card codes")
            logger.debug(f"Amazon gift card codes: {amazon_cards}")
        except ValueError as e:
            logger.error(str(e))

    # Close Selenium browser
    browser.quit()

    # **************************************************************
    # Build message that is going to be stored and/or sent
    # **************************************************************
    message = (
        build_tango_cards_message(tango_cards=tango_cards)
        + "\n\n"
        + build_amazon_cards_message(amazon_cards=amazon_cards)
    )
    logger.debug(f"Message: {message}")
    # Get path of the file that is going to store the message
    message_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results.txt"))
    # Store message in a file
    logger.info("Storing scraping results in a file...")
    try:
        store_message(message=message, file_path=message_file_path)
        logger.info("Scraping results stored successfully")
    except IOError as e:
        logger.error(str(e))
    # Send message if Telegram report sending is enabled
    if config.telegram.get("enable", False):
        logger.info("Sending scraping results to Telegram...")
        try:
            send_message_to_telegram(
                message=message, token=config.telegram.get("token", ""), chat_id=config.telegram.get("chat_id", "")
            )
            logger.info("Scraping results sent successfully to Telegram")
        except RequestException as e:
            logger.error(str(e))

    logger.info("All done! Exiting...")


if __name__ == "__main__":
    main()
