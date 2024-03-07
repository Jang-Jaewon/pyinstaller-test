from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.api import user, win
from app.core.config import ALLOWED_ORIGINS, APP_ENV, DEBUG
from app.core.database import engine

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"INFO:     Hello, Run in the {APP_ENV} environment 👋")
    yield
    print(f"INFO:     Bye, Shut down in the {APP_ENV} environment 👋")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(win.router)


@app.get("/api-health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "APP_ENV": APP_ENV,
        "DEBUG": DEBUG,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
