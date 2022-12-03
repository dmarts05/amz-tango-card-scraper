# Amazon Tango Card Gmail Scrapper

An automated solution for getting Amazon Gift Card codes from Microsoft Rewards emails.

## Installation

- Clone the repo.
- Install requirements with the following command:

```
pip install -r requirements.txt
```

- Make sure you have Chrome installed.

- Edit account.json.sample with the GMAIL email credentials of the account that you want the script to run on, and rename it by removing .sample at the end. Visit https://myaccount.google.com/apppasswords after enabling 2FA to get the required password. The syntax is the following:

```json
[
  {
    "username": "email@gmail.com",
    "password": "GoogleAppPassword"
  }
]
```

- Edit email.json.sample with your GMAIL email credentials. Again, visit https://myaccount.google.com/apppasswords after enabling 2FA to get the required password and rename it by removing .sample at the end. The syntax is the following:

```json
[
  {
    "sender": "sender@example.com",
    "password": "GoogleAppPassword",
    "receiver": "receiver@example.com"
  }
]
```

- Due to limits of Ipapi sometimes it returns error and it causes bot stops. You can define a default language and location to prevent it.

- Run the script.

## Optional arguments

- `--headless ` Run the script in headless mode.
- `--trash` Move to trash read emails.
- `--emailalerts` Enable GMAIL email alerts when obtaining codes.
