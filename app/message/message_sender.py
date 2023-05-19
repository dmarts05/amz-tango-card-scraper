"""Module for sending messages."""
import requests
from requests.exceptions import RequestException


def send_message_to_telegram(message: str, token: str, chat_id: str) -> None:
    """
    Send message to Telegram.

    Args:
        message: Message to send.

    Raises:
        RequestException: If the message could not be sent to Telegram.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url).json()
    if not response["ok"]:
        raise RequestException("Message could not be sent to Telegram")
