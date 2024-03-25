from pydantic import BaseModel, Field
from datetime import datetime


class ImageBase(BaseModel):
    pass


class ImageResponseSchema(ImageBase):
    id: int = Field(title="로컬 PC 이름", description="참여자 이름")
    path: str = Field(title="로컬 PC 이름", description="참여자 이름")
    created_by: str = Field(title="로컬 PC 이름", description="참여자 이름")
    created_at: datetime = Field(title="생성 일시", description="생성 일시")
    updated_at: datetime = Field(title="수정 일시", description="수정 일시")
    deleted_at: datetime | None = Field(None, title="삭제 일시", description="삭제 일시")

    class Config:
        from_attributes = True
