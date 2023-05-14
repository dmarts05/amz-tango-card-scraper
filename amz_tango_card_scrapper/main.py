import os

from utils.config_reader import ConfigReader


def main():
    # Get program configuration
    try:
        # Get path to config file
        config_path = get_config_file_path("config.yml")

        # Read config file
        config_reader = ConfigReader(config_path)
        config = config_reader.read_config()
        print(config)
    except ValueError as e:
        print(e)
        exit(1)
    except FileNotFoundError:
        print("Config file not found")
        exit(1)
    except OSError:
        print("Error reading config file")
        exit(1)


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


if __name__ == "__main__":
    main()
