"""
Extract Microsoft Rewards Amazon Gift Cards from Gmail automatically.
"""

import imaplib
import email
import json
import sys

from termcolor import cprint


def get_account_credentials():
    """Obtains account's credentials from "account.json".

    Returns:
        list: A list containing account's credentials.
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
    key = "FROM"
    value = "microsoftrewards@email.microsoftrewards.com"
    _, data = mail.search(None, key, value)

    # Get IDs of emails
    ids = data[0].split()

    # Capture all messages from emails
    messages = []
    for id in ids:
        typ, data = mail.fetch(id, "(RFC822)")
        messages.append(data)

    # Get tango security codes and links from each message
    tango_credentials = []
    for message in messages[::-1]:
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

    return tango_credentials


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
        print(tango_credentials)
        for credential in tango_credentials:
            print("Selenium part...")


if __name__ == "__main__":
    main()
