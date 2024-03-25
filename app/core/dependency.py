import socket

from sqlalchemy.orm import Session
from fastapi import Request

from app.core.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_client_info(request: Request):
    client_host = request.client.host
    try:
        host_name, _, _ = socket.gethostbyaddr(client_host)
    except socket.herror:
        host_name = "Unknown"

    return {"ip": client_host, "host_name": host_name}
