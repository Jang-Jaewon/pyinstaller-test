from sqlalchemy import Column, Integer, String

from app.api.models.base import Timestamp
from app.core.database import Base


class File(Base, Timestamp):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, comment="ID")
    image_path = Column(String, comment="파일 경로")
    created_by = Column(String, comment="생성 위치")
