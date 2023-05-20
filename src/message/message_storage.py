"""Module for storing messages."""


def store_message(message: str, file_path: str) -> None:
    """
    Stores the message in the specified file path.

    Args:
        message: the message to store
        file_path: the file path where the message will be stored

    Raises:
        IOError: If the message could not be stored
    """
    try:
        with open(file_path, "w") as f:
            f.write(message)
    except IOError:
        raise IOError("Message could not be stored")
