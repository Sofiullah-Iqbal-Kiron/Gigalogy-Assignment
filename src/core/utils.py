# python
import smtplib
from email.message import EmailMessage


GMAIL_USER = "sofiul.k.1023@gmail.com"
GMAIL_PASSWORD = "yqmn jcpt cvln upvw"


def send_verification_email(email: str, token: str):
    confirm_url = f"https://accounts.gigalogy.com/verify-email/?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Gigalogy Email Verification"
    msg["From"] = GMAIL_USER
    msg["To"] = email
    msg.set_content(
        f"Welcome! Please click the link below to verify your email:\n\n{confirm_url}\n\n"
        "This link expires in 1 hour."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
