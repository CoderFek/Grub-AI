from fastapi import FastAPI
from api.routes import subscribe, send
from api.db import init_db
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #change this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscribe.router, prefix="")
app.include_router(send.router, prefix="")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
def on_startup():
    init_db()
