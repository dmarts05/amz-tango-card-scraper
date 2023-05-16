"""Module that contains the schemas used in the project."""

from typing import Dict, List, NamedTuple


class ConfigFile(NamedTuple):
    """
    A schema that encapsulates the structure of the config file.

    gmail: the Gmail section of the config file
    amazon: the Amazon section of the config file
    from_list: the From section of the config file
    script: the Script section of the config file
    """

    gmail: Dict[str, str]
    amazon: Dict[str, str]
    from_list: List[str]
    script: Dict[str, bool]


class TangoCard(NamedTuple):
    """
    A schema that represents a tango card.

    security_code: the security code of the tango card
    tango_link: the link that will be used to redeem the tango card
    amazon_link: the link that will be used to redeem the amazon gift card
    """

    security_code: str
    tango_link: str
    amazon_link: str
