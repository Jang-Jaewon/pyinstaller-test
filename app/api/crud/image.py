from sqlalchemy.orm import Session
from app.api.models.image import Image


def create_image(image_path: str, host_name: str, db: Session):
    image_obj = Image(path=image_path, created_by=host_name)
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj
