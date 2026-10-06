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
EMAIL_TO = EMAIL_USERNAME

STATE_FILE = "page_hash.txt"


def get_page_content():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    return soup.get_text(
        "\n",
        strip=True
    )


def calculate_hash(content):

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def send_email():

    message = MIMEMultipart()

    message["From"] = EMAIL_USERNAME
    message["To"] = EMAIL_TO
    message["Subject"] = "🚨 Nouveau résultat Master - FS UIT"

    body = f"""
Bonjour,

Une modification a été détectée sur la page officielle
des résultats des Masters 2026/2027 de la Faculté des Sciences
de l'Université Ibn Tofaïl.

Consultez immédiatement la page :

{URL}

Une nouvelle liste de résultats, liste d'admission ou
mise à jour importante peut avoir été publiée.

Bonne chance !
"""

    message.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )

    print("Connecting to Gmail SMTP...")

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            EMAIL_USERNAME,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_USERNAME,
            EMAIL_TO,
            message.as_string()
        )

    print("Email sent successfully!")


def main():

    print("Checking FS UIT Master results...")
    print(f"URL: {URL}")

    content = get_page_content()

    current_hash = calculate_hash(
        content
    )

    old_hash = None

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            old_hash = file.read().strip()

    # First run
    if old_hash is None:

        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(current_hash)

        print("Initial page state saved.")
        print("No email sent on first run.")

        return

    # Change detected
    if current_hash != old_hash:

        print("CHANGE DETECTED!")

        send_email()

        with open(
            STATE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(current_hash)

        print("New state saved.")

    else:

        print("No change detected.")


if __name__ == "__main__":
    main()
