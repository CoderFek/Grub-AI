from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlmodel import Session, select
from typing import Annotated
import os
from cron_job import run_cron

from api.db import get_session
from api.models import Subscriber
from api.ai.poem_service import generate_email_message
from api.email_utils import send_poem_email

router = APIRouter()

# @router.post("/send-poem")
# def send_poem_to_verified_users(background_tasks: BackgroundTasks, session: Annotated[Session, Depends(get_session)]):
#     subscribers = session.exec(select(Subscriber).where(Subscriber.is_verified == True)).all()

#     for user in subscribers:
#         background_tasks.add_task(send_poem_email, user)

#     return {"message": f"Queued {len(subscribers)} emails"}

@router.get("/run-poem-cron", include_in_schema=False)
def trigger_poem_cron(request: Request, session: Session = Depends(get_session)):
    secret_key = request.query_params.get("key")
    expected_key = os.environ.get("CRON_SECRET_KEY")
    if secret_key != expected_key:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    run_cron(session)
    return {"status": "ok"}