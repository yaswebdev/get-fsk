import os
import hashlib
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://fs.uit.ac.ma/avis-aux-candidats-retenus-aux-masters-2026-2027/"

EMAIL_USERNAME = os.environ["EMAIL_USERNAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

# Send notification to this address
EMAIL_TO = EMAIL_USERNAME

STATE_FILE = "page_hash.txt"


def get_page_content():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/154 Safari/537.36"
        )
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove things that commonly change without meaning
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    return soup.get_text("\n", strip=True)


def calculate_hash(content):
    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def send_email():
    message = MIMEMultipart()

    message["From"] = EMAIL_USERNAME
    message["To"] = EMAIL_TO
    message["Subject"] = "🚨 New Master Result - FS UIT"

    body = f"""
A new change has been detected on the Faculty of Sciences
Master results page.

Check the page immediately:

{URL}

The page may contain a new admission/result announcement.
"""

    message.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_USERNAME,
            EMAIL_TO,
            message.as_string()
        )


def main():
    content = get_page_content()
    current_hash = calculate_hash(content)

    old_hash = None

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            old_hash = f.read().strip()

    # First run: save the current state without sending an alert
    if old_hash is None:
        with open(STATE_FILE, "w") as f:
            f.write(current_hash)

        print("Initial page state saved.")
        return

    # Something changed
    if current_hash != old_hash:
        print("CHANGE DETECTED!")

        send_email()

        with open(STATE_FILE, "w") as f:
            f.write(current_hash)

    else:
        print("No change.")


if __name__ == "__main__":
    main()
