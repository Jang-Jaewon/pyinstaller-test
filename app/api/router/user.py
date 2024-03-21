from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schema.base import RouterTags
from app.api.schema.user import (ItemCreateRequestSchema, ItemResponseSchema,
                                 UserCreateRequestSchema, UserResponseSchema)
from app.api.service import user as user_service
from app.core.dependency import get_db

router = APIRouter(prefix="/user", tags=[RouterTags.user])


@router.post("", status_code=201, response_model=UserResponseSchema, summary="사용자 생성",
)
def create_user(body: UserCreateRequestSchema, db: Session = Depends(get_db)):
    return user_service.create_user(body, db)


@router.get("", status_code=200, response_model=list[UserResponseSchema], summary="사용자 목록 조회",)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.read_users(skip, limit, db)


@router.get("/items", status_code=200, response_model=list[ItemResponseSchema], summary="아이템 목록 조회",)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.read_items(skip, limit, db)


@router.get("/{user_id}", status_code=200, response_model=UserResponseSchema, summary="사용자 상세 조회",)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.read_user(user_id, db)


@router.post("/{user_id}/items", status_code=201, response_model=ItemResponseSchema, summary="사용자별 아이템 생성",)
def create_item_for_user(
    user_id: int, body: ItemCreateRequestSchema, db: Session = Depends(get_db)
):
    return user_service.create_item_for_user(user_id, body, db)
