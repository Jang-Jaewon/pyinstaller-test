from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.api.models.base import Timestamp


class Image(Base, Timestamp):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    path = Column(String, comment="파일 경로")
    created_by = Column(String, comment="생성 위치")
