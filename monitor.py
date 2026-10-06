import os
import smtplib
from email.mime.text import MIMEText

username = os.environ["EMAIL_USERNAME"]
password = os.environ["EMAIL_PASSWORD"]

message = MIMEText(
    "This is a test email from your GitHub Actions Master Result Monitor."
)

message["Subject"] = "TEST - Master Result Monitor"
message["From"] = username
message["To"] = username

print("Connecting to Gmail SMTP...")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(username, password)
    print("Gmail authentication successful.")
    server.sendmail(username, username, message.as_string())

print("Email sent successfully!")
