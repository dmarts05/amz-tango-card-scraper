import platform

import requests
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
)


class ChromeBrowser:
    def __init__(
        self,
        headless: bool = True,
        no_images: bool = True,
        no_webdriver_manager: bool = False,
    ) -> None:
        self._headless = headless
        self._no_images = no_images
        self._no_webdriver_manager = no_webdriver_manager
        self._options = self._build_browser_options()
        self._browser = None

    def __enter__(self) -> Chrome:
        self.browser = (
            Chrome(options=self._options)
            if self._no_webdriver_manager
            else Chrome(
                service=Service(ChromeDriverManager().install()),
                options=self._options,
            )
        )
        return self.browser

    def __exit__(self) -> None:
        if self._browser:
            self._browser.quit()

    def _get_language(self) -> str:
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

    def _build_browser_options(self) -> ChromeOptions:
        options = ChromeOptions()

        # Add user agent and language to the browser options
        options.add_argument("user-agent=" + USER_AGENT)  # type: ignore # noqa
        options.add_argument("lang=" + self._get_language().split("-")[0])  # type: ignore # noqa

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
        if self._no_images:
            prefs["profile.managed_default_content_settings.images"] = 2
        options.add_experimental_option("prefs", prefs)  # type: ignore
        options.add_experimental_option("useAutomationExtension", False)  # type: ignore # noqa
        options.add_experimental_option(  # type: ignore
            "excludeSwitches", ["enable-automation"]
        )
        # Add headless option if specified
        if self._headless:
            options.add_argument("--headless")  # type: ignore

        # Add options specific to Linux
        if platform.system() == "Linux":
            options.add_argument("--no-sandbox")  # type: ignore
            options.add_argument("--disable-dev-shm-usage")  # type: ignore

        return options
