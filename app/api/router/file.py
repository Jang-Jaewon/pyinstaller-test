from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core.dependency import get_db, get_client_info
from app.api.service.file import save_file_on_disk
from app.api.schema.file import FileResponseSchema
from app.api.schema.base import RouterTags


router = APIRouter(prefix="/file", tags=[RouterTags.file])


@router.post(
    "/upload",
    status_code=201,
    response_model=FileResponseSchema,
    summary="이미지 전송 및 저장",
)
def upload_file(
        file: UploadFile = File(...),
        client_info: dict = Depends(get_client_info),
        db: Session = Depends(get_db)
):
    return save_file_on_disk(file, client_info, db)
