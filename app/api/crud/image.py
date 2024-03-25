from sqlalchemy.orm import Session

from app.api.models.file import File


def create_file(file_path: str, host_name: str, db: Session):
    file_obj = File(image_path=file_path, created_by=host_name)
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj
