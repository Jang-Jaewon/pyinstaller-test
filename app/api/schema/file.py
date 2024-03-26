from datetime import datetime

from pydantic import BaseModel, Field


class FileBase(BaseModel):
    pass


class FileResponseSchema(FileBase):
    id: int = Field(title="ID", description="ID")
    image_path: str = Field(title="파일 경로", description="파일 경로")
    image_name: str = Field(title="파일 이름", description="파일 이름")
    created_by: str = Field(title="생성 위치", description="생성 위치")
    created_at: datetime = Field(title="생성 일시", description="생성 일시")
    updated_at: datetime = Field(title="수정 일시", description="수정 일시")
    deleted_at: datetime | None = Field(
        None, title="삭제 일시", description="삭제 일시"
    )

    class Config:
        from_attributes = True
