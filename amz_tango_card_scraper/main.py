"""Module containing the main function of the program."""

import os
from amz_tango_card_scraper.browser import get_browser

from gmail_scraper import scrape_tango_cards
from config_reader import ConfigReader
from schemas import ConfigFile
from tango_scraper import scrap_amazon_gift_cards


def get_config_file_path(file_name: str) -> str:
    """
    Returns the path to the config file with the given name.

    Args:
        file_name: the name of the config file

    Returns:
        The path to the config file with the given name
    """
    # Get the parent directory of the current file
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Construct the path to the config file in the parent directory
    config_path = os.path.join(parent_dir, file_name)

    return config_path


def get_config(file_name: str) -> ConfigFile:
    """
    Returns the configuration of the program.

    Args:
        file_name: the name of the config file

    Returns:
        The configuration of the program
    """
    try:
        # Get path to config file
        config_file_path = get_config_file_path(file_name)

        # Read config file
        config_reader = ConfigReader(config_file_path)
        config = config_reader.read_config()
        return config
    except ValueError as e:
        print(e)
        exit(1)
    except FileNotFoundError:
        print("[ERROR] Configuration file 'config.yml' not found")
        exit(1)
    except OSError:
        print("[ERROR] Error reading configuration file")
        exit(1)


def main() -> None:
    # Get program configuration
    print("[INFO] Reading configuration file...")
    config = get_config("config.yml")
    print("[INFO] Configuration file read successfully")

    # Scrape Tango Cards from Gmail
    print("[INFO] Scraping Tango Cards from Gmail...")
    tango_cards = scrape_tango_cards(
        config.gmail.get("email", ""),
        config.gmail.get("app_password", ""),
        config.from_list,
        config.script.get("trash", False),
    )
    print("[INFO] Tango Cards scraped successfully")

    # Get Selenium browser
    browser = get_browser(
        config.script.get("headless", True),
        config.script.get("no_images", True),
        config.script.get("no_webdriver_manager", False),
    )

    # Scrape Amazon gift card codes from Tango Cards
    print("[INFO] Scraping Amazon gift card codes from Tango Cards...")
    amazon_cards = scrap_amazon_gift_cards(browser, tango_cards)
    print("[INFO] Amazon gift card codes scraped successfully")

    # Print Amazon gift card codes
    amazon_cards_str = "\n".join([str(card) for card in amazon_cards])
    print(amazon_cards_str)

    # Close Selenium browser
    browser.quit()


if __name__ == "__main__":
    main()
