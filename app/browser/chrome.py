"""Module for creating Selenium Chrome browser instances."""

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from .options import get_chrome_browser_options


def get_chrome_browser(
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
    options = get_chrome_browser_options(headless, no_images)
    browser = (
        Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if not no_webdriver_manager
        else Chrome(options=options)
    )
    return browser
