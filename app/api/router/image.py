from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependency import get_db
from app.api.service.image import save_image_on_disk


router = APIRouter()


@router.post("/images")
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image = save_image_on_disk(db, file)
    return {"filename": file.filename, "path": image.path}
