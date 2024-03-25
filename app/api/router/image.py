from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependency import get_db, get_client_info
from app.api.service.image import save_image_on_disk
from app.api.schema.image import ImageResponseSchema


router = APIRouter()


@router.post(
    "/images",
    status_code=201,
    response_model=ImageResponseSchema,
    summary="이미지 전송 및 저장",
)
def upload_image(
        file: UploadFile = File(...),
        client_info: dict = Depends(get_client_info),
        db: Session = Depends(get_db)
):
    return save_image_on_disk(file, client_info, db)
