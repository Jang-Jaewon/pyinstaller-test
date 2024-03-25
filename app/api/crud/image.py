from sqlalchemy.orm import Session
from app.api.models.image import Image


def create_image(db: Session, image_path: str):
    image_obj = Image(path=image_path, created_by="test_bed")
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj
