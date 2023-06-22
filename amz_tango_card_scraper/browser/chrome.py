"""Module for creating Selenium Chrome browser instances."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from undetected_chromedriver import Chrome  # type: ignore

from .options import get_chrome_browser_options

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


def get_chrome_browser(
    headless: bool = False,
    no_images: bool = False,
    proxies: List[str] = [],
) -> WebDriver:
    """
    Returns a configured Chrome browser instance.

    Args:
        headless: whether to run the browser in headless mode
        no_images: whether to disable images

    Returns:
        A Chrome browser instance
    """
    options = get_chrome_browser_options(headless, no_images, proxies)
    return Chrome(options=options)
