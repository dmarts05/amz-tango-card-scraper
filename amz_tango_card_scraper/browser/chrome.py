"""Module for creating Selenium Chrome browser instances."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

from .options import get_chrome_browser_options

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


def get_chrome_browser(
    headless: bool = True,
    no_images: bool = True,
    no_webdriver_manager: bool = False,
    proxies: List[str] = [],
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
    options = get_chrome_browser_options(headless, no_images, proxies)
    browser = (
        Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if not no_webdriver_manager
        else Chrome(options=options)
    )
    # Enable stealth mode for the browser to avoid detection
    stealth(
        browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return browser
