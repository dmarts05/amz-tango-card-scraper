"""Module to scrape Tango Cards from Gmail."""

import email as em
import imaplib
from typing import List

from schemas import TangoCard

IMAP_GMAIL_URL = "imap.gmail.com"
EMAIL_FORMAT = "(RFC822)"


def scrape_tango_cards(
    email: str, app_password: str, from_emails: List[str], trash: bool = False
) -> List[TangoCard]:
    """
    Scrapes Tango Cards from Gmail using the specified email addresses.

    Args:
        email: the email address to use to connect to Gmail
        app_password: the app password to use to connect to Gmail
        from_emails: a list of email addresses from which to check for
                     Tango Card emails
        trash: whether to trash the Tango Card emails after scraping them

    Returns:
        A list of Tango Cards
    """

    # Connection with Gmail using SSL
    with imaplib.IMAP4_SSL(IMAP_GMAIL_URL) as mail:
        # Login to Gmail
        mail.login(email, app_password)

        # Select Inbox to search for Tango Card emails
        mail.select("Inbox")

        # Search for Tango Card emails
        tango_cards: List[TangoCard] = []
        for from_email in from_emails:
            # Search for Tango Card emails from the specified email address
            _, data = mail.search(None, "FROM", from_email)
            email_ids = data[0].split()

            # If there are no Tango Card emails, next email address
            if not email_ids:
                continue

            # Capture all messages from the obtained email ids
            msgs = [mail.fetch(id, EMAIL_FORMAT)[1] for id in email_ids]

            # Get tango security code and links from the messages
            for id, msg in zip(email_ids, msgs):
                # Get response part of the message
                for response_part in msg:
                    # If the response part is not a tuple
                    # then continue with the next response part
                    if not isinstance(response_part, tuple):
                        # This means that the response part does not
                        # contain information about the Tango Card
                        continue

                    # Get the message content from the response part
                    msg_content = em.message_from_bytes(response_part[1])

                    # Get code and links from the body of the message
                    for part in msg_content.walk():
                        text = part.get_payload()

                        # Check if the text has multiple parts
                        if isinstance(text, list):
                            # This probably means that the text has been
                            # forwarded
                            # We only need the last part of the text in
                            # this case (the body)
                            text = (  # type: ignore
                                text[-1].get_payload().replace("=\r\n", "")  # type: ignore # noqa: E501
                            )

                            security_code = text.split(  # type: ignore
                                'tango-credential-value">'
                            )[4].split("<", 1)[0]

                            tango_link = text.split(  # type: ignore
                                'tango-credential-key"><a href=3D"', 1
                            )[1].split('"', 1)[0]

                        else:
                            security_code = text.split(
                                "</div><div class='tango-credential-value'>",
                                1,
                            )[1].split("<", 1)[0]

                            tango_link = text.split(
                                (
                                    "</div><div"
                                    " class='tango-credential-key'><a"
                                    " href='"
                                ),
                                1,
                            )[1].split("'", 1)[0]

                        amazon_link = (  # type: ignore
                            "https://www.amazon."
                            + text.split("http://www.amazon.", 1)[1].split(  # type: ignore # noqa: E501
                                "/",
                                1,
                            )[
                                0
                            ]
                        )

                        # Add Tango Card to the list
                        tango_cards.append(
                            TangoCard(
                                security_code, tango_link, amazon_link  # type: ignore # noqa: E501
                            )
                        )

                        if trash:
                            # Move email to trash
                            id = id.decode() if isinstance(id, bytes) else id
                            mail.store(id, "+FLAGS", "\\Deleted")

                        break
    return tango_cards
