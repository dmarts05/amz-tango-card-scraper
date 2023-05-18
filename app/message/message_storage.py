"""Module for storing messages."""


def store_message(message: str, file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write(message)
