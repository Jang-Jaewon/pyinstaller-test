from fastapi import HTTPException

import app.api.crud.user
from app.api.crud import user as user_crud


def create_user(body, db):
    db_user = user_crud.get_user_by_email(body.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(body, db)


def read_users(skip, limit, db):
    users = user_crud.get_users(skip, limit, db)
    return users


def read_items(skip, limit, db):
    items = app.api.crud.user.get_items(skip, limit, db)
    return items


def read_user(user_id, db):
    db_user = user_crud.get_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def create_item_for_user(user_id, body, db):
    item = app.api.crud.user.create_user_item(user_id, body, db)
    return item
