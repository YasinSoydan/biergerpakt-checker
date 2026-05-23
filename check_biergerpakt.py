import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# Keywords to detect September Orientation Day opening
KEYWORDS = [
    "orientation day",
    "journée d'orientation",
    "orientatiounsdag",
]
SEPTEMBER_KEYWORDS = ["september", "septembre", "september"]
URL = "https://biergerpakt.zesummeliewen.lu/en/new-2/welcome-to-the-biergerpakt/"

def fetch_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text.lower()

def is_september_orientation_open(page_text):
    has_orientation = any(kw in page_text for kw in KEYWORDS)
    has_september = any(kw in page_text for kw in SEPTEMBER_KEYWORDS)
    return has_orientation and has_september

def send_email(sender, password, recipient):
    subject = "🎉 Biergerpakt September Orientation Day — Registration is OPEN!"
    body = f"""Hi Dusty,

The September Orientation Day registration appears to be open on the Biergerpakt website.

Go register now:
{URL}

This alert was triggered on {datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}.

Good luck!
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Alert email sent to {recipient}")

def main():
    print(f"Checking Biergerpakt at {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}...")
    
    page_text = fetch_page()
    
    if True:  # TEST MODE - remove this line after confirming email works
        print("September Orientation Day detected — sending alert!")
        sender = os.environ["OUTLOOK_EMAIL"]
        password = os.environ["OUTLOOK_PASSWORD"]
        recipient = os.environ.get("ALERT_EMAIL", sender)
        send_email(sender, password, recipient)
    else:
        print("No September Orientation Day found yet. Will check again tomorrow.")

if __name__ == "__main__":
    main()
