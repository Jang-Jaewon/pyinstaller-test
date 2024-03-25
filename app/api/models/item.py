from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.api.models.base import Timestamp
from app.core.database import Base


class Item(Base, Timestamp):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    title = Column(String, comment="제목")
    description = Column(String, comment="설명")
    owner_id = Column(Integer, ForeignKey("users.id"), comment="사용자 ID")

    owner = relationship("User", back_populates="items")
