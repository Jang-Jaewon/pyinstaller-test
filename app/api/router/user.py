from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schema.base import RouterTags
from app.api.schema.user import (ItemCreateRequestSchema, ItemResponseSchema,
                                 UserCreateRequestSchema, UserResponseSchema)
from app.api.service import user as user_service
from app.core.dependency import get_db

router = APIRouter(prefix="/user", tags=[RouterTags.user])


@router.post("", response_model=UserResponseSchema)
def create_user(body: UserCreateRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(body, db)


@router.get("", response_model=list[UserResponseSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.read_users(skip, limit, db)


@router.get("/items", response_model=list[ItemResponseSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.read_items(skip, limit, db)


@router.get("/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.read_user(user_id, db)


@router.post("/{user_id}/items", response_model=ItemResponseSchema)
def create_item_for_user(
    user_id: int, body: ItemCreateRequestSchema, db: Session = Depends(get_db)
):
    return user_service.create_item_for_user(user_id, body, db)
