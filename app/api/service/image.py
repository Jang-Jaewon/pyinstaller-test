import os

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.crud.image import create_image


FILE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def save_image_on_disk(db: Session, file: UploadFile):
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    file_location = os.path.join(FILE_DIR, file.filename)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return create_image(db, file_location)
