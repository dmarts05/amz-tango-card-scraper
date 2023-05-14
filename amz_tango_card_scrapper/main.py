import os

from utils.config_reader import ConfigReader
from utils.types import ConfigFile


def get_config_file_path(file_name: str) -> str:
    """
    Returns the path to the config file with the given name.

    Args:
        file_name: the name of the config file

    Returns:
        The path to the config file with the given name
    """
    # Get the parent directory of the current file
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Construct the path to the config file in the parent directory
    config_path = os.path.join(parent_dir, file_name)

    return config_path


def get_config(file_name: str) -> ConfigFile:
    try:
        # Get path to config file
        config_file_path = get_config_file_path(file_name)

        # Read config file
        config_reader = ConfigReader(config_file_path)
        config = config_reader.read_config()
        return config
    except ValueError as e:
        print(e)
        exit(1)
    except FileNotFoundError:
        print("[ERROR] Configuration file 'config.yml' not found")
        exit(1)
    except OSError:
        print("[ERROR] Error reading configuration file")
        exit(1)


def main() -> None:
    # Get program configuration
    config = get_config("config.yml")
    print(config)


if __name__ == "__main__":
    main()
