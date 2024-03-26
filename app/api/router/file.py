from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.api.schema.base import RouterTags, CursorPagination
from app.api.schema.file import FileResponseSchema
from app.api.service import file as file_service
from app.core.dependency import get_client_info, get_db

router = APIRouter(prefix="/file", tags=[RouterTags.file])


@router.post(
    "",
    status_code=201,
    response_model=FileResponseSchema,
    summary="이지미 파일 전송 및 저장",
)
def upload_file(
    file: UploadFile = File(...),
    client_info: dict = Depends(get_client_info),
    db: Session = Depends(get_db),
):
    return file_service.save_file_on_disk(file, client_info, db)


@router.get(
    "",
    status_code=200,
    response_model=List[FileResponseSchema],
    summary="이미지 파일 목록 조회",
)
def get_files(
    pagination: CursorPagination = Depends(),
    db: Session = Depends(get_db),
):
    return file_service.get_files(pagination, db)
