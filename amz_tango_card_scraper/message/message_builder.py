"""Module for building messages."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from amz_tango_card_scraper.utils.schemas import AmazonCard, TangoCard


def build_tango_cards_message(tango_cards: List[TangoCard]) -> str:
    """
    Builds a message that contains the tango cards.

    Args:
        tango_cards: the tango cards that will be included in the message

    Returns:
        A message that contains the tango cards
    """
    # Early return if there are no tango cards
    if len(tango_cards) == 0:
        return ""

    title = "****************\n" + "*  TANGO CARDS  *\n" + "****************\n"
    body = "\n\n".join([str(i + 1) + " - " + str(tc) for i, tc in enumerate(tango_cards)])
    return title + body


def build_amazon_cards_message(amazon_cards: List[AmazonCard]) -> str:
    """
    Builds a message that contains the amazon cards.

    Args:
        amazon_cards: the amazon cards that will be included in the message

    Returns:
        A message that contains the amazon cards
    """
    # Early return if there are no amazon cards
    if len(amazon_cards) == 0:
        return ""

    title = "******************\n" + "*  AMAZON CARDS  *\n" + "******************\n"
    body = "\n\n".join([str(i + 1) + " - " + str(tc) for i, tc in enumerate(amazon_cards)])

    # Check if any of the cards has not been redeemed
    if any([not ac.redeem_status for ac in amazon_cards]):
        # Add a message to the body that explains how to redeem the cards
        body += f"\n\nYou can redeem the Amazon gift cards here: {amazon_cards[0].amazon_link}/gc/redeem"

    return title + body
