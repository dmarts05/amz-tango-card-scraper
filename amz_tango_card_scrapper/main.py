"""Module containing the main function of the program."""

import os

from gmail_scraper import GmailScraper
from utils.config_reader import ConfigReader
from utils.types import ConfigFile


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
    gmail_scraper = GmailScraper(
        config.gmail.get("email", ""), config.gmail.get("app_password", "")
    )
    print("[INFO] Scraping Tango Cards from Gmail...")
    tango_cards = gmail_scraper.scrape_tango_cards(
        config.from_list, config.script.get("trash", False)
    )
    print("[INFO] Tango Cards scraped successfully")
    print(tango_cards)


if __name__ == "__main__":
    main()
