from sqlalchemy import Column, Integer, String

from app.core.database import Base
from app.api.models.base import Timestamp


class Network(Base, Timestamp):
    __tablename__ = "network"

    id = Column(Integer, primary_key=True)
    hostname = Column(String, index=True)
    local_ip = Column(String, index=True)
    is_server = Column(String, index=True)
