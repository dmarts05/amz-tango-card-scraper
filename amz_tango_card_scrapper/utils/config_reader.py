"""Module for reading the config file."""

import yaml

from typing import Dict, List, Union, cast


class ConfigReader:
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path

    def read_config(
        self,
    ) -> Dict[str, Union[Dict[str, str], List[str], Dict[str, bool]]]:
        """
        Reads the config file and returns a dictionary with the following keys:
        - gmail: a dictionary with the following keys:
            - email: the email address of the Gmail account to use
            - app_password: the app password of the Gmail account to use
        - [Optional] amazon: a dictionary with the following keys:
            - email: the email address of the Amazon account to use
            - password: the password of the Amazon account to use
            - otp: the OTP of the Amazon account to use
        - from: a list of email addresses from which to check for Tango Card
                emails
        - script: a dictionary with the following keys:
            - no_images: whether to disable images in the Selenium browser
            - headless: whether to run the Selenium browser in headless mode
            - trash: whether to trash the Tango Card emails after redeeming
            - redeem: whether to automatically redeem the Tango Cards in
                      Amazon after scraping them

        Raises:
            - ValueError: if the config file is invalid

        Returns:
            A dictionary with the keys described above
        """

        config = {}
        with open(self._config_path, "r") as f:
            yaml_config = yaml.safe_load(f)

            # Verify and extract Gmail section
            gmail = self._verify_gmail_section(yaml_config["gmail"])
            config["gmail"] = gmail

            # Verify and extract Amazon section (if present)
            if "amazon" in yaml_config:
                amazon = self._verify_amazon_section(yaml_config["amazon"])
                config["amazon"] = amazon

            # Verify and extract From section
            from_list = self._verify_from_section(yaml_config["from"])
            config["from"] = from_list

            # Verify and extract Script section
            script = self._verify_script_section(yaml_config["script"])
            config["script"] = script

        return cast(
            Dict[str, Union[Dict[str, str], List[str], Dict[str, bool]]],
            config,
        )

    def _verify_gmail_section(self, gmail: Dict[str, str]) -> Dict[str, str]:
        required_fields = ("email", "app_password")
        if not all(field in gmail for field in required_fields):
            raise ValueError(
                "Missing required field(s) in Gmail section of config file."
            )
        return gmail

    def _verify_amazon_section(self, amazon: Dict[str, str]) -> Dict[str, str]:
        required_fields = ("email", "password", "otp")
        if not all(field in amazon for field in required_fields):
            raise ValueError(
                "Missing required field(s) in Amazon section of config file."
            )
        return amazon

    def _verify_from_section(self, from_list: List[str]) -> List[str]:
        # Check if the list is empty
        if not from_list:
            raise ValueError(
                "Empty from section in config file. Please add at least one"
                " email address."
            )
        return from_list

    def _verify_script_section(
        self, script: Dict[str, bool]
    ) -> Dict[str, bool]:
        required_fields = ("no_images", "headless", "trash", "redeem")
        if not all(field in script for field in required_fields):
            raise ValueError(
                "Missing required field(s) in Script section of config file."
            )
        return script
