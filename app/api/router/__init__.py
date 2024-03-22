from fastapi import APIRouter

from .user import router as user_router
from .win import router as win_router


api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(win.router)
