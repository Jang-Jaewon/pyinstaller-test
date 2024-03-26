import os

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.crud import file as file_crud
from app.api.schema.file import FileResponseSchema


def save_file_on_disk(file: UploadFile, client_info: dict, db: Session):
    host_name = client_info.get("host_name")
    file_name = file.filename
    file_dir = os.path.join(os.path.dirname(__file__), "..", "images", host_name)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, file_name)

    with open(file_path, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_crud.create_file(file_path, file_name, host_name, db)


def get_files(pagination, db: Session):
    cursor_id = pagination.cursor_id
    page_size = pagination.page_size
    files = file_crud.get_files(cursor_id, page_size, db)
    return [FileResponseSchema.from_orm(file) for file in files]


def get_file(file_id: int, db: Session):
    file_obj = file_crud.get_file_by_id(file_id, db)
    if not file_obj:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path=file_obj.image_path, filename=file_obj.image_name)