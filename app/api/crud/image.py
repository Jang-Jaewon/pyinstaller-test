from sqlalchemy.orm import Session
from app.api.models.file import File


def create_file(image_path: str, host_name: str, db: Session):
    image_obj = File(path=image_path, created_by=host_name)
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj
