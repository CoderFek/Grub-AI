from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends
from sqlmodel import Session, select
from typing import Annotated

from api.db import get_session
from api.models import Subscriber
from api.ai.schemas import SubscriptionRequest, SubscriptionResponse, EmailMessageSchema, PoemRequest
from api.email_utils import send_verification_email
from api.email_utils import send_welcome_email
from fastapi import Form



router = APIRouter()

# @router.get("/")
# def health():
#     return {"status": "ok"}

@router.post("/subscribe", response_model=SubscriptionResponse)
def subscribe_user(
    payload: SubscriptionRequest,
    background_tasks: BackgroundTasks,
    session: Annotated[Session, Depends(get_session)]
):
    email = payload.email.lower()

    # Check for duplicates
    existing = session.exec(select(Subscriber).where(Subscriber.email == email)).first()
    if existing:
        return SubscriptionResponse(message="Already subscribed or pending verification.")

    new_subscriber = Subscriber(email=email)
    session.add(new_subscriber)
    session.commit()
    session.refresh(new_subscriber)

    # Send verification email asynchronously
    background_tasks.add_task(send_verification_email, new_subscriber)

    return SubscriptionResponse(message="Verification email sent.")

@router.get("/api/verify-email")
def verify_email(token: str, session: Annotated[Session, Depends(get_session)]):
    subscriber = session.exec(select(Subscriber).where(Subscriber.verification_token == token)).first()

    if not subscriber:
        raise HTTPException(status_code=400, detail="Invalid token")

    if not subscriber.is_verified:
        subscriber.is_verified = True
        session.add(subscriber)
        session.commit()

    return {"email": subscriber.email}

@router.post("/set-frequency")
def set_frequency(
    email: str = Form(...),
    frequency: str = Form(...),
    session: Session = Depends(get_session)
):
    subscriber = session.exec(select(Subscriber).where(Subscriber.email == email)).first()

    if not subscriber or not subscriber.is_verified:
        raise HTTPException(status_code=400, detail="Invalid or unverified user")

    if subscriber.frequency:
        return {"message": "Frequency already set."}

    subscriber.frequency = frequency
    session.add(subscriber)
    session.commit()

    send_welcome_email(
        to_email=email,
        frequency=frequency,
        subscribed_at=subscriber.subscribed_at
    )

    return {"message": "Frequency set successfully."}
