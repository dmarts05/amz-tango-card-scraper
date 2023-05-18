"""Module that contains the schemas used in the project."""

from typing import Dict, List, NamedTuple


class ConfigFile(NamedTuple):
    """
    A schema that encapsulates the structure of the config file.

    gmail: the Gmail section of the config file
        - email: the email address of the Gmail account
        - app_password: the app password of the Gmail account
    amazon: the Amazon section of the config file
        - email: the email address of the Amazon account
        - password: the password of the Amazon account
        - otp: the OTP of the Amazon account
    from_list: the From section of the config file with a list of email
        addresses for filtering
    script: the Script section of the config file
        - no_images: whether to disable images in the browser
        - headless: whether to run the browser in headless mode
        - trash: whether to trash the emails after scraping
        - redeem_amz: whether to redeem the amazon gift cards
        - no_webdriver_manager: whether to disable the webdriver manager
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

    def __str__(self) -> str:
        """
        Returns a string representation of the tango card.

        Returns:
            A string representation of the tango card
        """
        return (
            f"[Tango Card]\nSecurity code: {self.security_code}\nTango link:"
            f" {self.tango_link}\nAmazon link: {self.amazon_link}"
        )


class AmazonCard(NamedTuple):
    """
    A schema that represents an amazon gift card.

    redeem_code: the code of the amazon gift card
    amazon_link: the link that will be used to redeem the amazon gift card
    """

    redeem_code: str
    amazon_link: str

    def __str__(self) -> str:
        """
        Returns a string representation of the amazon gift card.

        Returns:
            A string representation of the amazon gift card
        """
        return (
            f"[Amazon Gift Card]\nRedeem code: {self.redeem_code}\nAmazon"
            f" link: {self.amazon_link}"
        )
