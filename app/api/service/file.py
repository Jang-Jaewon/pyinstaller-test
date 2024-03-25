import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.crud.image import create_file

FILE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def save_file_on_disk(file: UploadFile, client_info: dict, db: Session):
    print(client_info)
    host_name = client_info.get("host_name")
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    file_path = os.path.join(FILE_DIR, file.filename)

    with open(file_path, "wb+") as file_object:
        file_object.write(file.file.read())
    return create_file(file_path, host_name, db)
