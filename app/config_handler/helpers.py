"""Module that contains helper functions for the config handler."""

from typing import Dict, List

import yaml


def parse_config(file_path: str):
    """
    Parse the config file and return a ConfigFile object that contains the
    parsed config file.

    Refer to :class:`ConfigFile` for more information.

    Args:
        file_path: Path to the config file.

    Raises:
        ValueError: If the config file is invalid.

    Returns:
        A ConfigFile that contains the parsed config file.
    """
    from app.utils.schemas import ConfigFile

    with open(file_path, "r") as f:
        yaml_config = yaml.safe_load(f)

        # Verify and extract Gmail section
        gmail = verify_gmail_section(yaml_config.get("gmail", {}))

        # Verify and extract Amazon section
        amazon = verify_amazon_section(yaml_config.get("amazon", {}))

        # Verify and extract From section
        from_list = verify_from_section(yaml_config.get("from", []))

        # Verify and extract Script section
        script = verify_script_section(yaml_config.get("script", {}))

        # Verify and extract Telegram section
        telegram = verify_telegram_section(yaml_config.get("telegram", {}))

    return ConfigFile(gmail=gmail, amazon=amazon, from_list=from_list, script=script, telegram=telegram)


def verify_gmail_section(gmail: Dict[str, str]) -> Dict[str, str]:
    """
    Verify the Gmail section of the config file.

    Args:
        gmail: The Gmail section of the config file.

    Raises:
        ValueError: If the Gmail section is invalid.

    Returns:
        The verified Gmail section of the config file.
    """
    required_fields = ("email", "app_password")
    if not all(field in gmail for field in required_fields):
        raise ValueError("Missing required field(s) in Gmail section of config file.")
    return gmail


def verify_amazon_section(amazon: Dict[str, str]) -> Dict[str, str]:
    """
    Verify the Amazon section of the config file.

    Args:
        amazon: The Amazon section of the config file.

    Raises:
        ValueError: If the Amazon section is invalid.

    Returns:
        The verified Amazon section of the config file.
    """

    required_fields = ("email", "password", "otp")
    if not all(field in amazon for field in required_fields):
        raise ValueError("Missing required field(s) in Amazon section of config file.")
    return amazon


def verify_from_section(from_list: List[str]) -> List[str]:
    """
    Verify the From section of the config file.

    Args:
        from_list: The From section of the config file.

    Raises:
        ValueError: If the From section is invalid.

    Returns:
        The verified From section of the config file.
    """

    # Check if the list is empty
    if not from_list:
        raise ValueError("Empty from section in config file. Please add at least one" " email address.")
    return from_list


def verify_script_section(script: Dict[str, bool]) -> Dict[str, bool]:
    """
    Verify the Script section of the config file.

    Args:
        script: The Script section of the config file.

    Raises:
        ValueError: If the Script section is invalid.

    Returns:
        The verified Script section of the config file.
    """
    required_fields = (
        "no_images",
        "headless",
        "trash",
        "redeem_amz",
        "no_webdriver_manager",
    )
    if not all(field in script for field in required_fields):
        raise ValueError("Missing required field(s) in Script section of config file.")
    return script


def verify_telegram_section(telegram: Dict[str, str]) -> Dict[str, str]:
    """
    Verify the Telegram section of the config file.

    Args:
        telegram: The Telegram section of the config file.

    Raises:
        ValueError: If the Telegram section is invalid.

    Returns:
        The verified Telegram section of the config file.
    """

    required_fields = ("enable", "token", "chat_id")
    if not all(field in telegram for field in required_fields):
        raise ValueError("Missing required field(s) in Telegram section of config file.")
    return telegram
