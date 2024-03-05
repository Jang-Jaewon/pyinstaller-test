from contextlib import asynccontextmanager

import uvicorn
from app.core.config import APP_ENV, DEBUG, ALLOWED_ORIGINS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


@app.get("/api-health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "APP_ENV": APP_ENV,
        "DEBUG": DEBUG,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
