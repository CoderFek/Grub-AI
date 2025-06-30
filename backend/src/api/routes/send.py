from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from typing import Annotated

from api.db import get_session
from api.models import Subscriber
from api.ai.poem_service import generate_email_message
from api.email_utils import send_poem_email

router = APIRouter()

@router.post("/send-poem")
def send_poem_to_verified_users(background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]):
    subscribers = session.exec(select(Subscriber).where(Subscriber.verified == True)).all()

    for user in subscribers:
        background_tasks.add_task(send_poem_email, user)

    return {"message": f"Queued {len(subscribers)} emails"}
