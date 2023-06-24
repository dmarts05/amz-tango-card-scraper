"""Module to scrape Tango Cards from Gmail."""

import email as em
import imaplib
from typing import List

from amz_tango_card_scraper.utils.logger import setup_logger
from amz_tango_card_scraper.utils.schemas import TangoCard

from .constants import IMAP_GMAIL_URL
from .helpers import extract_tango_card_from_body, get_body_of_email

logger = setup_logger(logger_name=__name__)


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
    # Establish connection with Gmail
    mail = imaplib.IMAP4_SSL(IMAP_GMAIL_URL)
    # Login to Gmail
    mail.login(email, app_password)
    # Select Inbox to search for Tango Card emails
    mail.select("inbox")

    tango_cards: List[TangoCard] = []
    # Search for Tango Card emails from the specified email addresses
    for from_address in from_list:
        logger.info(f"Searching for Tango Cards from {from_address}...")
        # Fetch all emails from the specified email address
        _, msg_ids = mail.search(None, "FROM", from_address)

        # Iterate over all the emails
        for msg_id in msg_ids[0].split():
            # Fetch the email data (RFC822) for the given ID
            _, msg_data = mail.fetch(msg_id, "(RFC822)")

            # Get the status of the email
            _, flags_data = mail.fetch(msg_id, "(FLAGS)")

            # Iterate over all the responses
            for response in msg_data:
                # Check if the response is a tuple (contains the email data)
                if isinstance(response, tuple):
                    msg = em.message_from_bytes(response[1])
                    # Check if email has been read, if so, skip it
                    if "\\Seen" in flags_data[0].decode("utf-8"):  # type: ignore
                        logger.info(f"Skipping email {msg_id.decode('utf-8')} as it has already been read...")
                        continue

                    body = get_body_of_email(msg)

                    # Check if body contains Tango Card
                    if "tango" in body:
                        logger.info(f"Tango Card found in email {msg_id.decode('utf-8')}")
                        # If it does, extract the Tango Card
                        tango_cards.append(extract_tango_card_from_body(body))

                        # Trash the email if specified
                        if trash:
                            logger.info(f"Trashing email {msg_id.decode('utf-8')}...")
                            mail.store(msg_id, "+X-GM-LABELS", "\\Trash")

    mail.close()
    return tango_cards
