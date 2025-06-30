import os
import requests
from api.ai.poem_service import generate_email_message

from api.models import Subscriber

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL")  # e.g. verified@yourdomain.com
BREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME", "Daily Poems")
DOMAIN = os.environ.get("DOMAIN")

if not BREVO_API_KEY or not BREVO_SENDER_EMAIL:
    raise RuntimeError("Brevo credentials are not set")

def send_verification_email(subscriber: Subscriber) -> None:
    token = subscriber.verification_token
    verify_link = f"https://{DOMAIN}/verify-email?token={token}"

    data = {
        "sender": {
            "name": BREVO_SENDER_NAME,
            "email": BREVO_SENDER_EMAIL
        },
        "to": [{"email": subscriber.email}],
        "subject": "Verify your email to receive daily poems",
        "htmlContent": f"""
        <p>Hello,</p>
        <p>Thank you for subscribing! Please <a href="{verify_link}">click here to verify your email</a>.</p>
        <p>If you didn’t request this, you can ignore this message.</p>
        """
    }

    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=data,
        headers=headers
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Failed to send email: {response.status_code} - {response.text}")


def send_poem_email(subscriber: Subscriber) -> None:
    poem = generate_email_message("Write a new daily poem")

    data = {
        "sender": {
            "name": BREVO_SENDER_NAME,
            "email": BREVO_SENDER_EMAIL
        },
        "to": [{"email": subscriber.email}],
        "subject": poem.subject,
        "textContent": poem.content
    }

    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=data,
        headers=headers
    )

    if response.status_code >= 400:
        raise RuntimeError(f"Failed to send poem email: {response.status_code} - {response.text}")
