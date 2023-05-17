"""Module for creating Selenium Chrome browser instances."""

import platform
from typing import Tuple

import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
)


def get_browser_language() -> str:
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


def get_browser_options(
    headless: bool = True, no_images: bool = True
) -> Options:
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
    options.add_experimental_option(  # type: ignore
        "excludeSwitches", ["enable-automation"]
    )
    # Add headless option if specified
    if headless:
        options.add_argument("--headless")  # type: ignore

    # Add options specific to Linux
    if platform.system() == "Linux":
        options.add_argument("--no-sandbox")  # type: ignore
        options.add_argument("--disable-dev-shm-usage")  # type: ignore

    return options


def get_browser(
    headless: bool = True,
    no_images: bool = True,
    no_webdriver_manager: bool = False,
) -> WebDriver:
    """
    Returns a configured Chrome browser instance.

    Args:
        headless: whether to run the browser in headless mode
        no_images: whether to disable images
        no_webdriver_manager: whether to disable the webdriver manager

    Returns:
        A Chrome browser instance
    """
    options = get_browser_options(headless, no_images)
    browser = (
        Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        if not no_webdriver_manager
        else Chrome(options=options)
    )
    return browser


def wait_for_element(
    browser: WebDriver, locator: Tuple[str, str], timeout: int = 15
) -> WebElement:
    wait = WebDriverWait(browser, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))  # type: ignore # noqa
    return element  # type: ignore
