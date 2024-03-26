from enum import Enum

from pydantic import BaseModel, Field


class RouterTags(Enum):
    user = "user"
    win = "win"
    file = "file"


class CursorPagination(BaseModel):
    cursor_id: int = Field(0, alias="cursor", description="현재 커서 위치")
    page_size: int = Field(20, alias="page_size", description="페이지 당 항목 수", ge=1, le=200)

