from app.api.models.item import Item
from app.api.models.user import User


def get_user(user_id, db):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(email, db):
    return db.query(User).filter(User.email == email).first()


def get_users(skip, limit, db):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(user, db):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(skip, limit, db):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(user_id, body, db):
    db_item = Item(**body.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
