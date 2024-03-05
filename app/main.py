import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.setting import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"INFO:     Hello, Run in the {settings.APP_ENV} environment 👋")
    yield
    print(f"INFO:     Bye, Shut down in the {settings.APP_ENV} environment 👋")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api-health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "debug-mode": settings.DEBUG,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
