"""Module for testing proxies.py"""

from amz_tango_card_scraper.browser.proxies import is_proxy_working


def test_is_proxy_working():
    # Test case 1: proxy is not working
    proxy = "http://invalid.proxy.example.com:8080"
    assert not is_proxy_working(proxy)
