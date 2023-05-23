"""Module for getting browser options for Selenium."""

import platform

import requests
from selenium.webdriver.chrome.options import Options
from typing import List
from .proxies import get_random_working_proxy

from amz_tango_card_scraper.utils.logger import setup_logger

logger = setup_logger(__name__)


def get_browser_language() -> str:
    """
    Get the user's browser language.

    Returns:
        The user's browser language
    """
    try:
        # Get the user's IP address
        response = requests.get("https://api.ipify.org?format=json")
        ip = response.json()["ip"]

        # Use the ipapi API to get the user's location data
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        location_data = response.json()

        # Get the user's language preference
        lang = location_data["languages"].split(",")[0]
    except requests.exceptions.RequestException:
        # If the API request fails, default to English
        lang = "en-US"

    return lang


def get_chrome_browser_options(headless: bool = True, no_images: bool = True, proxies: List[str] = []) -> Options:
    """
    Returns a configured Chrome browser options instance.

    Args:
        headless: whether to run the browser in headless mode
        no_images: whether to disable images

    Returns:
        A Chrome browser options instance
    """
    from .constants import USER_AGENT

    options = Options()

    # Add user agent and language to the browser options
    options.add_argument("user-agent=" + USER_AGENT)  # type: ignore # noqa
    options.add_argument("lang=" + get_browser_language().split("-")[0])  # type: ignore # noqa

    # Add misc options
    options.add_argument("--disable-blink-features=AutomationControlled")  # type: ignore # noqa
    options.add_argument("log-level=3")  # type: ignore
    options.add_argument("--start-maximized")  # type: ignore
    prefs = {
        "profile.default_content_setting_values.geolocation": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False,
    }
    # Add no images option if specified
    if no_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    options.add_experimental_option("prefs", prefs)  # type: ignore
    options.add_experimental_option("useAutomationExtension", False)  # type: ignore # noqa
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # type: ignore
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
