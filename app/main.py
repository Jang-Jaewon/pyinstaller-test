from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.setting import APP_ENV, DEBUG, ALLOWED_ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"INFO:     Hello, Run in the {APP_ENV} environment 👋")
    yield
    print(f"INFO:     Bye, Shut down in the {APP_ENV} environment 👋")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api-health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "debug-mode": DEBUG,
        # "debug-mode": settings.DEBUG,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/env_test")
def read_env():
    return {
        "APP_ENV": APP_ENV,
        "DEBUG": DEBUG,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
