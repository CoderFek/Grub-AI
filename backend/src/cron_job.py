# cron_job.py — run this file once per day (via GitHub Actions or any scheduler)

from datetime import datetime, timezone
from sqlmodel import Session, select
from api.db import get_session
from api.models import Subscriber
from api.ai.poem_service import generate_email_message
from api.email_utils import send_poem_email
import random

themes = [
    "Moon", "Romance", "Rain", "Nature", "Stars", "Inspirational", "Sunset", "Twilight"
]


def should_send_today(subscriber: Subscriber) -> bool:
    if subscriber.frequency == "daily":
        return True
    elif subscriber.frequency == "weekly":
        return datetime.now(timezone.utc).weekday() == 0  # Monday
    return False

def run_cron(session: Session):
    print("📬 Starting daily poem job...")

    subscribers = session.exec(
        select(Subscriber).where(
            Subscriber.is_verified == True,
            Subscriber.frequency.is_not(None)
        )
    ).all()

    for sub in subscribers:
        if should_send_today(sub):
            theme = random.choice(themes)
            try:
                prompt = f"Write a short cozy poem about {theme.lower()}"
                poem = generate_email_message(prompt)
                send_poem_email(sub.email, poem, theme, sub.frequency)
                print(f"✅ Sent poem to {sub.email} [Theme: {theme}]")
            except Exception as e:
                print(f"❌ Failed to send to {sub.email}: {e}")

    print("✅ Poem job complete.")

if __name__ == "__main__":
    session: Session = next(get_session())
    run_cron(session)
