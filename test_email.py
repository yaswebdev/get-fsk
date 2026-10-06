import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USERNAME = os.environ["EMAIL_USERNAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

message = MIMEText(
    """Hello!

This is a TEST email from your GitHub Actions Master Result Monitor.

If you received this email, Gmail SMTP is working correctly.

Your Master Result Monitor can now send notifications automatically.
"""
)

message["Subject"] = "TEST - Master Result Monitor"
message["From"] = EMAIL_USERNAME
message["To"] = EMAIL_USERNAME

print("Connecting to Gmail...")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(
        EMAIL_USERNAME,
        EMAIL_PASSWORD
    )

    print("Gmail login successful.")

    server.sendmail(
        EMAIL_USERNAME,
        EMAIL_USERNAME,
        message.as_string()
    )

print("TEST EMAIL SENT SUCCESSFULLY!")
