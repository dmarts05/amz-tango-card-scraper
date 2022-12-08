# Amazon Tango Card Gmail Scrapper

An automated solution for getting Amazon Gift Card codes from Microsoft Rewards emails.

## Installation

- Clone the repo.

- Install requirements with the following command:

```
pip install -r requirements.txt
```

- Make sure you have Chrome installed.

- Edit account.json.sample with the GMAIL email credentials of the account that you want the script to run on, and rename it by removing .sample at the end of the file name. Visit https://myaccount.google.com/apppasswords after enabling 2FA to get the required password. The syntax is the following:

```json
[
  {
    "username": "email@gmail.com",
    "password": "GoogleAppPassword"
  }
]
```

- Edit email.json.sample with your GMAIL email credentials if you want to receive email alerts. Again, visit https://myaccount.google.com/apppasswords after enabling 2FA to get the required password and rename it by removing .sample at the end of the file name. The syntax is the following:

```json
[
  {
    "sender": "sender@example.com",
    "password": "GoogleAppPassword",
    "receiver": "receiver@example.com"
  }
]
```

- Edit from.json.sample with the emails that will be able to send you Microsoft Rewards Tango Card emails (you can set up email forwarding to a single account and include those accounts in this json so they can be detected by the script). Don't forget to rename it by removing .sample at the end of the file name. The syntax is the following:

```json
[
  {
    "email": "microsoftrewards@email.microsoftrewards.com"
  },
  {
    "email": "email@example.com"
  }
]
```

- Edit amazon.json.sample with your Amazon credentials if you want to enable the auto-redeem feature (WIP). You'll need an OTP code from Amazon, refer to this webpage to obtain it: https://www.amazon.com/gp/help/customer/display.html?nodeId=G3PWZPU52FKN7PW4. Don't forget to rename it removing .sample at the end of the file name. The syntax is the following:

```json
[
  {
    "username": "email@example.com",
    "password": "pass1234",
    "otp": "OtpAmazonCode"
  }
]
```

- Due to limits of Ipapi sometimes it returns error and it causes bot stops. You can define a default language and location to prevent it (in the script).

- Run the script.

## Optional arguments

- `--headless ` Run the script in headless mode.
- `--trash` Move to trash read emails.
- `--emailalerts` Enable GMAIL email alerts when obtaining codes.
- `--redeem` Redeem obtained codes in amazon (WIP).
