from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.api.models.base import Timestamp
from app.core.database import Base


class User(Base, Timestamp):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    email = Column(String, unique=True, index=True, comment="이메일")
    hashed_password = Column(String, comment="비밀번호")
    is_active = Column(Boolean, default=True, comment="활성화 상태")

    items = relationship("Item", back_populates="owner")
