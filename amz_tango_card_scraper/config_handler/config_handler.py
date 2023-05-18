"""Module for handling the configuration file."""

from config_handler_helpers import parse_config
from schemas import ConfigFile


def get_config(file_path: str) -> ConfigFile:
    """
    Get the config file.

    Refer to :class:`ConfigFile` for more information.

    Args:
        file_path: Path to the config file.

    Returns:
        A ConfigFile that contains the parsed config file.
    """
    try:
        # Read config file
        config = parse_config(file_path)
        return config
    except ValueError as e:
        print(e)
        exit(1)
    except FileNotFoundError:
        print('[ERROR] Configuration file "config.yml" not found')
        exit(1)
