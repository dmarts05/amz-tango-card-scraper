"""Module for sending messages."""
import requests


def send_message_to_telegram(message: str, token: str, chat_id: str) -> None:
    """
    Send message to Telegram.

    Args:
        message: Message to send.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url).json()
    if not response["ok"]:
        print("[ERROR] Message could not be sent to Telegram")
    else:
        print("[INFO] Message sent successfully to Telegram")
