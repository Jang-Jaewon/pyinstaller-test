from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.api.models.base import Timestamp


class Image(Base, Timestamp):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    created_by = Column(String)
