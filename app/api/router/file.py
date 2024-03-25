from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.schema.base import RouterTags
from app.api.schema.file import FileResponseSchema
from app.api.service.file import save_file_on_disk
from app.core.dependency import get_client_info, get_db

router = APIRouter(prefix="/file", tags=[RouterTags.file])


@router.post(
    "/upload",
    status_code=201,
    response_model=FileResponseSchema,
    summary="이지미 파일 전송 및 저장",
)
def upload_file(
    file: UploadFile = File(...),
    client_info: dict = Depends(get_client_info),
    db: Session = Depends(get_db),
):
    return save_file_on_disk(file, client_info, db)
