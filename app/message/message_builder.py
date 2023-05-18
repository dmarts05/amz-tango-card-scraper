"""Module for building messages."""

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.utils.schemas import AmazonCard, TangoCard


def build_tango_cards_message(tango_cards: List["TangoCard"]) -> str:
    """
    Builds a message that contains the tango cards.

    Args:
        tango_cards: the tango cards that will be included in the message

    Returns:
        A message that contains the tango cards
    """
    title = (
        "******************************\n" + "*        TANGO CARDS         *\n" + "******************************\n"
    )
    body = "\n\n".join([str(i + 1) + " - " + str(tc) for i, tc in enumerate(tango_cards)])
    return title + body


def build_amazon_cards_message(amazon_cards: List["AmazonCard"]) -> str:
    """
    Builds a message that contains the amazon cards.

    Args:
        amazon_cards: the amazon cards that will be included in the message

    Returns:
        A message that contains the amazon cards
    """
    title = (
        "******************************\n" + "*        AMAZON CARDS        *\n" + "******************************\n"
    )
    body = "\n\n".join([str(i + 1) + " - " + str(tc) for i, tc in enumerate(amazon_cards)])
    return title + body
