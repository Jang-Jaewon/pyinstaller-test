from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import user, win
from app.core.middleware import ProcessTimeMiddleware
from app.core.config import ALLOWED_ORIGINS, APP_ENV, DEBUG
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)


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
app.add_middleware(ProcessTimeMiddleware)


api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(win.router)
app.include_router(api_router)


@app.get("/api/health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "APP_ENV": APP_ENV,
        "DEBUG": DEBUG,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
