"""
Extract Microsoft Rewards Amazon Gift Cards from Gmail automatically.
"""

from email.message import EmailMessage
import platform
import imaplib
import email
import json
import random
import smtplib
import ssl
import sys
from argparse import ArgumentParser
import time
import traceback

import ipapi
import pyotp

from termcolor import cprint

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display


def argument_parser():
    """Gets arguments from command line (--headless, ...)"""

    parser = ArgumentParser(
        description="Amazon Tango Card Gmail Scrapper",
        allow_abbrev=False,
        usage="You may execute the program with the default configuration or use arguments to configure available options.",
    )

    parser.add_argument(
        "--headless",
        help="Enable headless browser.",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--fakeheadless",
        help="Enable headless browser through a virtual display (Linux servers only). Avoid using headless and fakeheadless modes together.",
        action="store_true",
    )

    parser.add_argument(
        "--trash",
        help="Move checked emails to trash.",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--emailalerts",
        help="Send an email if some codes have been founds.",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--redeem",
        help="Redeem obtained codes in Amazon (WIP).",
        action="store_true",
        required=False,
    )

    arguments = parser.parse_args()

    return arguments


def get_lang_code():
    """Obtains language code of the user using ipapi.

    Returns:
        str: Language code of the user.
    """

    try:
        nfo = ipapi.location()
        lang = nfo["languages"].split(",")[0]
        return lang
    # ipapi may sometimes raise an exception due to its limitations, in that case, I default to en-US.
    except Exception:
        return "en-US"


def set_up_browser():
    """Sets up a Selenium chromium browser.

    Returns:
        WebDriver: Configured Selenium chromium browser.
    """

    arguments = argument_parser()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.24"
    options = Options()

    options.add_argument("user-agent=" + user_agent)
    options.add_argument("lang=" + get_lang_code())
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {
        "profile.default_content_setting_values.geolocation": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if arguments.headless:
        options.add_argument("--headless")
    options.add_argument("log-level=3")
    options.add_argument("--start-maximized")
    if platform.system() == "Linux":
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    chrome_browser_obj = None
    try:
        chrome_browser_obj = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    except Exception:
        chrome_browser_obj = webdriver.Chrome(options=options)
    finally:
        return chrome_browser_obj


def get_account_credentials():
    """Obtains account credentials from "account.json".

    Returns:
        list: A list containing account credentials.
    """
    try:
        account = json.load(open("account.json", "r"))[0]
        cprint("[ACCOUNT LOADER] Account successfully loaded.", "green")
        return account
    except FileNotFoundError:
        with open("account.json", "w") as f:
            f.write(
                json.dumps(
                    [
                        {
                            "username": "email@gmail.com",
                            "password": "GoogleAppPassword",
                        }
                    ],
                    indent=2,
                )
            )
        cprint('[ACCOUNT LOADER] "account.json" not found, creating file...', "red")
        print(
            '[ACCOUNT LOADER] Please fill you account creadentials in "account.json" and rerun the script. Exiting...'
        )
        sys.exit()


def get_email_credentials():
    """Obtains email credentials from "email.json".

    Returns:
        list: A list containing email credentials.
    """

    email_credentials = []
    try:
        email_credentials = json.load(open("email.json", "r"))[0]
    except FileNotFoundError:
        with open("email.json", "w") as f:
            f.write(
                json.dumps(
                    [
                        {
                            "sender": "sender@example.com",
                            "password": "GoogleAppPassword",
                            "receiver": "receiver@example.com",
                        }
                    ],
                    indent=2,
                )
            )
    finally:
        email_credentials = json.load(open("email.json", "r"))[0]
        return email_credentials


def get_from_addresses():
    """Obtains every allowed from email address from "from.json" to filter from.

    Returns:
        list: A list containing every allowed email address to filter from.
    """
    try:
        from_addresses = json.load(open("from.json", "r"))
    except FileNotFoundError:
        with open("from.json", "w") as f:
            f.write(
                json.dumps(
                    [
                        {
                            "email": "microsoftrewards@email.microsoftrewards.com",
                        }
                    ],
                    indent=2,
                )
            )
    finally:
        from_addresses = json.load(open("from.json", "r"))
        return from_addresses


def get_tango_credentials(username: str, password: str, from_addresses: list):
    """Obstains every tango credential from Microsoft emails in an account.

    Args:
        username (str): Account's Gmail email
        password (str): Account's Google App Password
        from_addresses (list): List of emails that will serve as a FROM filter when scrapping emails

    Returns:
        list: A list containing scrapped tango credentials
    """
    # URL for IMAP connection
    imap_url = "imap.gmail.com"

    # Connection with Gmail using SSL
    mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using credentials
    mail.login(username, password)

    # Select Inbox to fetch emails
    mail.select("Inbox")

    tango_credentials = []
    for from_address in from_addresses:
        # Email search
        status, data = mail.search(None, "FROM", from_address["email"])

        # Get IDs of emails
        ids = data[0].split()

        # Capture all messages from emails
        messages = []
        for id in ids:
            status, data = mail.fetch(id, "(RFC822)")
            messages.append(data)

        # Get tango security codes and links from each message
        counter = 0
        for message in messages:
            for response_part in message:
                if isinstance(response_part, tuple):
                    current_msg = email.message_from_bytes(response_part[1])

                    # Get code and link from the body of the email
                    for part in current_msg.walk():
                        text = part.get_payload()

                        # Check if the text has multiple parts
                        if isinstance(text, list):
                            # This probably means that the text has been forwarded
                            # We will need to use a different way of getting our Tango credentials

                            text = text[-1].get_payload().replace("=\r\n", "")

                            security_code = text.split('tango-credential-value">')[
                                4
                            ].split("<", 1)[0]

                            tango_link = text.split(
                                'tango-credential-key"><a href=3D"', 1
                            )[1].split('"', 1)[0]

                        else:

                            security_code = text.split(
                                "</div><div class='tango-credential-value'>", 1
                            )[1].split("<", 1)[0]

                            tango_link = text.split(
                                "</div><div class='tango-credential-key'><a href='", 1
                            )[1].split("'", 1)[0]

                        amazon_link = (
                            "https://www.amazon."
                            + text.split("http://www.amazon.",
                                         1)[1].split("/", 1)[0]
                        )

                        # Check required elements have been found
                        if security_code and tango_link and amazon_link:
                            tango_credential = {
                                "security_code": security_code,
                                "tango_link": tango_link,
                                "amazon_link": amazon_link,
                            }

                            tango_credentials.append(tango_credential)

                            current_msg_id = ids[counter]
                            if isinstance(current_msg_id, bytes):
                                # If it's a bytes type, decode to str
                                current_msg_id = current_msg_id.decode()

                            arguments = argument_parser()
                            if arguments.trash:
                                # Move current email to trash
                                mail.store(current_msg_id,
                                           "+X-GM-LABELS", "\\Trash")

                            break
            counter += 1

    mail.close()
    mail.logout()
    return tango_credentials


def get_amazon_gift_card_code(browser: WebDriver, credential: dict):
    """Gets an Amazon Gift Card Code given required Tango credentials.

    Args:
        browser (WebDriver): Selenium browser.
        credential (dict): Dictionary containing the required security code and link for redeeming a card.

    Returns:
        dict: Dictionary containing the code of an Amazon Gift Card and its Amazon Geo Link or an empty dictionary if it failed.
    """

    # Get to designated tango redeeming website
    browser.get(credential["tango_link"])
    # Long sleep time due to Tango "human verification"
    time.sleep(random.uniform(8, 11))

    print("[TANGO REDEEMER] Writing security code...")
    browser.find_element(
        By.XPATH,
        value="/html/body/div[1]/div/main/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/form/div[1]/div/div/div[1]/div/input",
    ).send_keys(credential["security_code"])

    print("[TANGO REDEEMER] Getting Amazon Gift Card...")
    browser.find_element(
        By.XPATH,
        value="/html/body/div[1]/div/main/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/form/div[2]/button",
    ).click()
    time.sleep(random.uniform(5, 8))

    # Check if card was correctly redeemed
    if browser.find_elements(
        By.XPATH,
        value="/html/body/div[1]/div[1]/main/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/span",
    ):
        code = browser.find_element(
            By.XPATH,
            value="/html/body/div[1]/div[1]/main/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/span",
        ).text
        code_info = {
            "code": code,
            "amazon_link": credential["amazon_link"],
            "redeemed": False,
        }
        cprint("[TANGO REDEEMER] Amazon Gift Card successfully obtained!", "green")
        return code_info

    cprint(
        "[TANGO REDEEMER] Credentials are not valid, Amazon Gift Card not obtained!",
        "red",
    )
    return {}


def store_codes(codes_info: list):
    """Stores obtained codes in "codes.txt".

    Args:
        codes_info (list): A list of Amazon Gift Card codes.
    """

    codes = map(lambda code_info: code_info["code"], codes_info)
    with open("codes.txt", "w") as f:
        cprint('[CODE STORER] Storing codes in "codes.txt"...', "green")
        for code in codes:
            f.write(code)
            f.write("\n")


def send_email(sender: str, receiver: str, password: str, codes_info: list):
    """Sends an email with obtained codes.

    Args:
        sender (str): Email sender.
        receiver (str): Email receiver.
        password (str): Google App Password of the sender.
        codes_info (list): A list of Amazon Gift Card codes.
    """

    arguments = argument_parser()
    subject = "Amazon Tango Card Gmail Scrapper has obtained some codes!"

    # Set body contents depending on whether the user has enabled auto-redeem
    body = ""
    if arguments.redeem:
        for code_info in codes_info:
            correctly_redeemed = code_info["redeemed"]
            if correctly_redeemed:
                body += code_info["code"] + " - ✅ Redeemed.\n"
            else:
                body += code_info["code"] + " - ❎ Not redeemed.\n"
    else:
        for code_info in codes_info:
            body += code_info["code"] + "\n"

    body += (
        "\nYou can try to redeem them yourself through this link: "
        + codes_info[0]["amazon_link"]
        + "/gc/redeem"
    )

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    ssl_context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as smtp:
        try:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, message.as_string())
            cprint("[EMAIL SENDER] Sending email with obtained codes...", "green")
        except:
            cprint("[EMAIL SENDER] Incorrect email or password!", "red")
            return


def is_same_amazon_geo_link_for_each_code(codes_info: list):
    """Checks if every code comes from the same location

    Args:
        codes_info (list): List of dictionaries that contain a code and its location

    Returns:
        boolean: True if every code comes from the same location, False if that's not the case
    """
    amazon_link = codes_info[0]["amazon_link"]
    for code_info in codes_info:
        if code_info["amazon_link"] != amazon_link:
            return False

    return True


def get_amazon_account_credentials():
    """Obtains Amazon account's credentials from "amazon.json".

    Returns:
        list: A list containing Amazon account's credentials.
    """

    try:
        account = json.load(open("amazon.json", "r"))[0]
        cprint("[AMAZON ACCOUNT LOADER] Amazon account successfully loaded.", "green")
        return account
    except FileNotFoundError:
        with open("amazon.json", "w") as f:
            f.write(
                json.dumps(
                    [
                        {
                            "username": "email@example.com",
                            "password": "pass1234",
                            "otp": "OtpAmazonCode",
                        }
                    ],
                    indent=2,
                )
            )
            cprint(
                '[AMAZON ACCOUNT LOADER] "amazon.json" not found, creating file...',
                "red",
            )
            print(
                '[AMAZON ACCOUNT LOADER] Please fill you account creadentials in "amazon.json" and rerun the script. Exiting...'
            )
            sys.exit()


def get_otp_code(otp_key: str):
    """Obtains an OTP code for the given key.

    Args:
        otp_key (str): Key that will generate the OTP code.

    Returns:
        int: OTP code for the given key.
    """

    return pyotp.TOTP(otp_key.strip().replace(" ", "")).now()


def sign_in_amazon(
    browser: WebDriver, username: str, pwd: str, otp_key: str, amazon_geo_link: str
):
    """Signs in the specified account using its credentials on Amazon.

    Args:
        browser (WebDriver): Selenium browser that will be used.
        username (str): Account's email.
        pwd (str): Account's password.
        otp_key (str): Account's OTP key.
    """

    # Strip https and www from amazon_geo_link
    amazon_geo_link = amazon_geo_link.replace(
        "https://", "").replace("www.", "")

    # Get to amazon login page
    print(amazon_geo_link)
    link = "https://www.{}/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.{}%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&".format(
        amazon_geo_link, amazon_geo_link)
    browser.get(link)
    time.sleep(random.uniform(5, 8))

    print("[SIGN IN] Writing email...")
    browser.find_element(By.ID, value="ap_email").send_keys(username)

    print("[SIGN IN] Writing password...")
    browser.find_element(By.ID, value="continue").click()
    time.sleep(random.uniform(5, 8))
    browser.find_element(By.ID, value="ap_password").send_keys(pwd)

    # Sign in (first step)
    browser.find_element(By.ID, value="signInSubmit").click()
    time.sleep(random.uniform(5, 8))

    print("[SIGN IN] Writing OTP...")
    try:
        otp_code = get_otp_code(otp_key)
    except Exception:
        print(traceback.format_exc())
        cprint("[SIGN IN] Error, malformed OTP key, exiting...", "red")
        sys.exit()
    browser.find_element(By.ID, value="auth-mfa-otpcode").send_keys(otp_code)

    # Sign in (second step)
    browser.find_element(By.ID, value="auth-signin-button").click()
    time.sleep(random.uniform(5, 8))

    # Check if we have managed to successfully sign in
    if browser.find_elements(
        By.XPATH, value="/html/body/div[1]/div[1]/div[2]/div/div[1]/div/div/div"
    ):
        # We are still in OTP verification form, OTP code is not valid
        cprint("[SIGN IN] Error, OTP code is not valid, exiting...", "red")
        sys.exit()


def redeem_amazon_gift_card_code(browser: WebDriver, code_info: dict):
    """Automatically redeems in Amazon a given code (user must already be signed in).

    Args:
        browser (WebDriver): Selenium browser that will be used.
        code_info (dict): Dictionary that contains the code that will be redeemed
                          and its Amazon Geo Link.
    """

    # Get to gift card redeeming site (already signed in)
    browser.get(code_info["amazon_link"] + "/gc/redeem")
    time.sleep(random.uniform(5, 8))

    print("[AMAZON REDEEMER] Writing code...")
    browser.find_element(By.ID, value="gc-redemption-input").send_keys(
        code_info["code"]
    )

    # TODO: Check for captchas and circunvent them

    print("[AMAZON REDEEMER] Redeeming code...")
    browser.find_element(By.ID, value="gc-redemption-apply-button").click()
    time.sleep(random.uniform(1, 2))

    # Check if code has been correctly redeemed
    if browser.find_elements(By.ID, value="gc-redemption-error"):
        code_info["redeemed"] = False
        cprint(
            "[AMAZON REDEEMER] " + code_info["code"] +
            " couldn't be redeemed!", "red"
        )
    else:
        code_info["redeemed"] = True
        cprint(
            "[AMAZON REDEEMER] " + code_info["code"] +
            " was successfully redeemed!",
            "green",
        )


def main():
    """
    Extract Microsoft Rewards Amazon Gift Cards from Gmail automatically.
    """
    # Get used arguments
    arguments = argument_parser()

    # Enable virtual display if fakeheadless argument is present and if headless argument is not present (Linux only)
    if (
        platform.system() == "Linux"
        and arguments.fakeheadless
        and not arguments.headless
    ):
        display = Display(visible=0, size=(800, 600))
        display.start()

    account = get_account_credentials()
    from_addresses = get_from_addresses()

    codes_info = []

    tango_credentials = get_tango_credentials(
        account["username"], account["password"], from_addresses
    )

    if not tango_credentials:
        cprint(
            "[TANGO SCRAPPER] No gift cards have been found, exiting...",
            "red",
        )
        sys.exit()

    # Set up Selenium browser
    try:
        browser = set_up_browser()
    except Exception:
        print(traceback.format_exc())
        cprint("[BROWSER] Error trying to set up browser...", "red")
        sys.exit()

    for tango_credential in tango_credentials:
        code_info = get_amazon_gift_card_code(browser, tango_credential)

        if code_info:
            codes_info.append(code_info)

    # Check if any codes have been obtained
    if codes_info:
        # If codes have been found, store them in "codes.txt"
        store_codes(codes_info)

        # Start auto-redeem in Amazon if the argument is present
        if arguments.redeem:
            if is_same_amazon_geo_link_for_each_code(codes_info):
                amazon_account = get_amazon_account_credentials()

                try:
                    sign_in_amazon(
                        browser,
                        amazon_account["username"],
                        amazon_account["password"],
                        amazon_account["otp"],
                        codes_info[0]["amazon_link"],
                    )

                    for code_info in codes_info:
                        redeem_amazon_gift_card_code(browser, code_info)
                except Exception:
                    print(traceback.format_exc())
                    cprint(
                        "[AMAZON REDEEMER] Amazon has detected that we are using a bot, stopping auto-redeem...",
                        "red",
                    )
            else:
                cprint(
                    "[AMAZON REDEEMER] Every code must come from the same localization, skipping auto-redeem...",
                    "red",
                )

        # Send email alerts if codes have been found and if email alerts have been activated
        if arguments.emailalerts:
            email_credentials = get_email_credentials()
            send_email(
                email_credentials["sender"],
                email_credentials["receiver"],
                email_credentials["password"],
                codes_info,
            )

        browser.quit()


if __name__ == "__main__":
    main()
