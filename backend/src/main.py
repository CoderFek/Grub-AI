from fastapi import FastAPI
from api.routes import subscribe, send
from api.db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscribe.router, prefix="")
app.include_router(send.router, prefix="")

@app.on_event("startup")
def on_startup():
    init_db()
