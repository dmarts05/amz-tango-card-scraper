"""Module to scrape Tango Cards from Gmail."""

import email as em
import imaplib
from email.message import Message
from typing import List

from bs4 import BeautifulSoup

from app.utils.schemas import TangoCard


def get_body_of_email(msg: Message) -> str:  # type: ignore
    """
    Get the body of an email.

    Args:
        msg: Email message.

    Returns:
        Body of the email.
    """
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # Skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True).decode("utf-8")
    else:
        return msg.get_payload(decode=True).decode("utf-8")


def extract_tango_card_from_body(body: str) -> TangoCard:
    """
    Extract Tango Card from the body of an email.

    Args:
        body: Body of the email.

    Returns:
        Extracted Tango Card.
    """
    from .constants import SECURITY_CODE_CLASS, TANGO_LINK_CLASS

    soup = BeautifulSoup(body, "html.parser")

    # Extract the security code
    security_code = soup.find_all("div", {"class": SECURITY_CODE_CLASS})[3].get_text()

    # Extract Tango link
    tango_link = soup.find_all("div", {"class": TANGO_LINK_CLASS})[3].find("a").get("href")

    # Extract Amazon link
    amazon_link = (  # type: ignore
        "https://www.amazon."
        + body.split("http://www.amazon.", 1)[1].split(  # type: ignore
            "/",
            1,
        )[0]
    )

    return TangoCard(security_code=security_code, tango_link=tango_link, amazon_link=amazon_link)  # type: ignore


def scrape_tango_cards(email: str, app_password: str, from_list: List[str], trash: bool = False) -> List[TangoCard]:
    """
    Scrape Tango Cards from Gmail using the IMAP protocol.

    Args:
        email: Gmail email address.
        app_password: Gmail app password.
        from_list: List of email addresses to search for Tango Cards.
        trash: Whether to trash the emails after scraping them.

    Returns:
        List of scraped Tango Cards.
    """
    from .constants import EMAIL_FORMAT, IMAP_GMAIL_URL

    # Establish connection with Gmail
    mail = imaplib.IMAP4_SSL(IMAP_GMAIL_URL)
    # Login to Gmail
    mail.login(email, app_password)
    # Select Inbox to search for Tango Card emails
    mail.select("inbox")

    tango_cards: List[TangoCard] = []
    # Search for Tango Card emails from the specified email addresses
    for from_address in from_list:
        # Fetch all emails from the specified email address
        _, msg_ids = mail.search(None, "FROM", from_address)

        # Iterate over all the emails
        for msg_id in msg_ids[0].split():
            # Fetch the email data (RFC822) for the given ID
            _, msg_data = mail.fetch(msg_id, EMAIL_FORMAT)

            # Iterate over all the responses
            for response in msg_data:
                # Check if the response is a tuple (contains the email data)
                if isinstance(response, tuple):
                    msg = em.message_from_bytes(response[1])
                    body = get_body_of_email(msg)

                    # Check if body contains Tango Card
                    if "tango" in body:
                        # If it does, extract the Tango Card
                        tango_cards.append(extract_tango_card_from_body(body))

                        # Trash the email if specified
                        if trash:
                            mail.store(msg_id, "+FLAGS", "\\Deleted")

    mail.close()
    return tango_cards
