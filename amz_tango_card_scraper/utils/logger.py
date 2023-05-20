"""Module containing the logger setup function."""
import logging
import os

LOG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "amz_tango_card_scraper.log"))


def reset_log_file(log_file: str = LOG_FILE_PATH) -> None:
    with open(log_file, "w") as f:
        f.write("")


def setup_logger(logger_name: str, log_file: str = LOG_FILE_PATH, level: int = logging.INFO) -> logging.Logger:
    """
    Setup a logger.

    Args:
        logger_name: Name of the logger.
        log_file: Path to the log file.
        level: Logging level.

    Returns:
        Logger object.
    """
    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
