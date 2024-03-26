import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.crud import file as file_crud
from app.api.schema.file import FileResponseSchema


FILE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def save_file_on_disk(file: UploadFile, client_info: dict, db: Session):
    host_name = client_info.get("host_name")
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    file_path = os.path.join(FILE_DIR, file.filename)

    with open(file_path, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_crud.create_file(file_path, host_name, db)


def get_files(pagination, db: Session):
    cursor_id = pagination.cursor_id
    page_size = pagination.page_size
    files = file_crud.get_files(cursor_id, page_size, db)
    return [FileResponseSchema.from_orm(file) for file in files]
