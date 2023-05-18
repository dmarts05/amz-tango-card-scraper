"""Extra actions for the browser."""

from typing import Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def wait_for_element(
    browser: WebDriver, locator: Tuple[str, str], timeout: int = 15
) -> WebElement:
    wait = WebDriverWait(browser, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))  # type: ignore # noqa
    return element  # type: ignore
