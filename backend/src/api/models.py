from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid


def generate_token() -> str:
    return str(uuid.uuid4())

def utcnow():
    return datetime.now(timezone.utc)


class Subscriber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    is_verified: bool = Field(default=False)
    verification_token: str = Field(default_factory=generate_token)
    subscribed_at: datetime = Field(default_factory=utcnow)
    frequency: Optional[str] = Field(default=None)  # "daily" or "weekly"
