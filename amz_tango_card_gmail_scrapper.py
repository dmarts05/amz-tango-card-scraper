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

from termcolor import cprint

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def argument_parser():
    """Gets arguments from command line (--headless, ...)"""

    parser = ArgumentParser(
        description="Amazon Tango Card Gmail Scrapper",
        allow_abbrev=False,
        usage="You may execute the program with the default configuration or use arguments to configure available options.",
    )

    parser.add_argument(
        "--headless",
        help="[Optional] Enable headless browser.",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--trash",
        help="[Optional] Move checked emails to trash.",
        action="store_true",
        required=False,
    )

    parser.add_argument(
        "--emailalerts",
        help="[Optional] Send an email if some codes have been founds.",
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


def get_tango_credentials(username: str, password: str):
    """Obstains every tango credential from Microsoft emails in an account.

    Args:
        username (str): Account's Gmail email
        password (str): Account's Google App Password

    Returns:
        list: List containing scrapped tango credentials
    """
    # URL for IMAP connection
    imap_url = "imap.gmail.com"

    # Connection with Gmail using SSL
    mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using credentials
    mail.login(username, password)

    # Select Inbox to fetch emails
    mail.select("Inbox")

    # Email search
    status, data = mail.search(
        None, "FROM", "microsoftrewards@email.microsoftrewards.com"
    )

    # Get IDs of emails
    ids = data[0].split()

    # Capture all messages from emails
    messages = []
    for id in ids:
        status, data = mail.fetch(id, "(RFC822)")
        messages.append(data)

    # Get tango security codes and links from each message
    tango_credentials = []
    counter = 0
    for message in messages:
        for response_part in message:
            if isinstance(response_part, tuple):
                current_msg = email.message_from_bytes(response_part[1])

                # Get code and link from the body of the email
                for part in current_msg.walk():
                    text = part.get_payload()

                    security_code = text.split(
                        "</div><div class='tango-credential-value'>", 1
                    )[1].split("<", 1)[0]

                    link = text.split(
                        "</div><div class='tango-credential-key'><a href='", 1
                    )[1].split("'", 1)[0]

                    # Check required elements have been found
                    if security_code and link:
                        tango_credential = {
                            "security_code": security_code,
                            "link": link,
                        }

                        tango_credentials.append(tango_credential)

                        current_msg_id = ids[counter]
                        if isinstance(current_msg_id, bytes):
                            # If it's a bytes type, decode to str
                            current_msg_id = current_msg_id.decode()

                        arguments = argument_parser()
                        if arguments.trash:
                            # Move current email to trash
                            mail.store(current_msg_id, "+X-GM-LABELS", "\\Trash")
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
        str: Code of the obstained card or an empty string if it failed.
    """

    # Get to designated tango redeeming website
    browser.get(credential["link"])
    time.sleep(random.uniform(2, 3))

    print("[TANGO REDEEMER] Writing security code...")
    browser.find_element(By.ID, value="input-45").send_keys(credential["security_code"])
    time.sleep(random.uniform(1, 2))

    print("[TANGO REDEEMER] Getting Amazon Gift Card...")
    browser.find_element(
        By.XPATH,
        value="/html/body/div[1]/div/main/div/div/div/div/div[1]/div/div/div[2]/div[2]/div/div/form/div[2]/button",
    ).click()
    time.sleep(random.uniform(2, 3))

    # Check if card was correctly redeemed
    if browser.find_elements(
        By.XPATH,
        value="/html/body/div[1]/div[1]/main/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/span",
    ):
        code = browser.find_element(
            By.XPATH,
            value="/html/body/div[1]/div[1]/main/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/span",
        ).text
        cprint("[TANGO REDEEMER] Amazon Gift Card successfully obtained!", "green")
        return code

    cprint(
        "[TANGO REDEEMER] Credentials are not valid, Amazon Gift Card not obtained!",
        "red",
    )
    return ""


def store_codes(codes: list):
    """Stores obtained codes in "codes.txt".

    Args:
        codes (list): A list of Amazon Gift Card codes.
    """

    with open("codes.txt", "w") as f:
        for code in codes:
            f.write(code)
            f.write("\n")


def send_email(sender: str, receiver: str, password: str, codes: list):
    """Sends an email with obtained codes.

    Args:
        sender (str): Email sender.
        receiver (str): Email receiver.
        password (str): Google App Password of the sender.
        codes (list): A list of Amazon Gift Card codes.
    """

    subject = "Amazon Tango Card Gmail Scrapper has obtained some codes!"
    body = "\n".join(codes)

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    ssl_context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as smtp:
        try:
            smtp.login(sender, password)
        except:
            cprint("[EMAIL SENDER] Incorrect email or password!", "red")
            return
        smtp.sendmail(sender, receiver, message.as_string())
        cprint("[EMAIL SENDER] Email with obtanied codes sent!", "green")


def main():
    """
    Extract Microsoft Rewards Amazon Gift Cards from Gmail automatically.
    """

    account = get_account_credentials()
    tango_credentials = get_tango_credentials(account["username"], account["password"])

    if not tango_credentials:
        cprint("[TANGO SCRAPPER] No cards have been found, exiting...", "red")
        sys.exit()
    else:
        codes = []
        for credential in tango_credentials:
            # Set up Selenium browser
            try:
                browser = set_up_browser()
            except Exception:
                print(traceback.format_exc())
                cprint("[BROWSER] Error trying to set up browser...", "red")
                sys.exit()

            code = get_amazon_gift_card_code(browser, credential)
            browser.quit()

            if code != "":
                codes.append(code)
            #     print('[CODE STORER] Storing in "codes.txt" obtained code...')
            #     store_code(code)

        if codes:
            # Send email alerts if codes have been found and email alerts have been activated
            arguments = argument_parser()
            if arguments.emailalerts:
                email_credentials = get_email_credentials()
                send_email(
                    email_credentials["sender"],
                    email_credentials["receiver"],
                    email_credentials["password"],
                    codes,
                )

            # If codes have been found, store them in "codes.txt"
            store_codes(codes)


if __name__ == "__main__":
    main()
