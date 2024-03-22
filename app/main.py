from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import create_schema
from app.core.middleware import ProcessTimeMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_schema()
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
app.add_middleware(ProcessTimeMiddleware)

app.include_router(api_router)


@app.get("/api/health-check")
def api_health_check():
    return {
        "api_server_status": f"{settings.APP_ENV} api-server is Ok",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
