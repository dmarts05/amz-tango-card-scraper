"""Module for getting browser options for Selenium."""

import platform
from typing import List

from undetected_chromedriver import ChromeOptions  # type: ignore

from amz_tango_card_scraper.utils.logger import setup_logger

from .proxies import get_random_working_proxy

logger = setup_logger(__name__)


def get_chrome_browser_options(
    headless: bool = False, no_images: bool = False, proxies: List[str] = []
) -> ChromeOptions:
    """
    Returns a configured Chrome browser options instance.

    Args:
        headless: whether to run the browser in headless mode
        no_images: whether to disable images

    Returns:
        A Chrome browser options instance
    """
    options = ChromeOptions()
    # Add no images option if specified
    if no_images:
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # type: ignore
    # Add headless option if specified
    if headless:
        options.add_argument("--headless")  # type: ignore
    # Add proxies if specified
    if proxies:
        proxy = get_random_working_proxy(proxies)
        # Only add a proxy if a working one was found
        if proxy:
            logger.info(f"Using proxy {proxy}")
            options.add_argument(f"--proxy-server={proxy}")  # type: ignore
        else:
            logger.warning("No working proxies found, defaulting to no proxy")

    # Add options specific to Linux
    if platform.system() == "Linux":
        options.add_argument("--no-sandbox")  # type: ignore
        options.add_argument("--disable-dev-shm-usage")  # type: ignore

    return options
