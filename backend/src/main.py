from fastapi import FastAPI
from api.routes import subscribe, send
from api.db import init_db

app = FastAPI()

app.include_router(subscribe.router, prefix="")
app.include_router(send.router, prefix="")

@app.on_event("startup")
def on_startup():
    init_db()
