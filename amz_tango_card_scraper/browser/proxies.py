import random
import requests

from typing import List
from requests.exceptions import RequestException


def is_proxy_working(proxy: str) -> bool:
    """
    Tests a proxy by making a request through it and checking the response status code.

    Args:
        proxy: the proxy server to test (e.g. "http://proxy.example.com:8080")

    Returns:
        True if the proxy is working, False otherwise
    """
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except RequestException:
        return False


def get_random_working_proxy(proxies: List[str]) -> str:
    """
    Returns a random working proxy from a list of proxies.

    Args:
        proxies: a list of proxies to choose from
        (e.g. ["http://proxy1.example.com:8080", "http://proxy2.example.com:8080"])

    Returns:
        A working proxy server (e.g. "http://proxy.example.com:8080"), or an empty string if no working proxy was found
    """
    random.shuffle(proxies)
    for proxy in proxies:
        if is_proxy_working(proxy):
            return proxy
    return ""
