from sqlalchemy import Boolean, Column, Integer, String

from app.api.models.base import Timestamp
from app.core.database import Base


class Network(Base, Timestamp):
    __tablename__ = "network"

    id = Column(Integer, primary_key=True, comment="ID")
    hostname = Column(String, comment="컴퓨터 이름")
    local_ip = Column(String, comment="로컬 IP 주소")
    is_server = Column(Boolean, default=False, comment="서버 여부")
