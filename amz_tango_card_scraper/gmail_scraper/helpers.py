from email.message import Message

from bs4 import BeautifulSoup

from amz_tango_card_scraper.utils.schemas import TangoCard

from .constants import SECURITY_CODE_CLASS, TANGO_LINK_CLASS


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
