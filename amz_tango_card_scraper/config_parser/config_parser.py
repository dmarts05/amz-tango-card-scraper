import yaml

from amz_tango_card_scraper.utils.schemas import ConfigFile

from .helpers import (
    verify_amazon_section,
    verify_from_section,
    verify_gmail_section,
    verify_script_section,
    verify_telegram_section,
)


def parse_config(file_path: str) -> ConfigFile:
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
