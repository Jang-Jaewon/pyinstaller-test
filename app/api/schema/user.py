from pydantic import BaseModel, EmailStr, Field


class ItemBase(BaseModel):
    title: str = Field(title="제목", description="제목")
    description: str | None = Field(None, title="설명", description="설명")


class ItemCreateRequestSchema(ItemBase):
    pass


class ItemResponseSchema(ItemBase):
    id: int = Field(title="ID", description="ID")
    owner_id: int = Field(title="소유자", description="소유자")

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr = Field(title="이메일", description="이메일")


class UserCreateRequestSchema(UserBase):
    password: str = Field(title="비밀번호", description="비밀번호")


class UserResponseSchema(UserBase):
    id: int = Field(title="ID", description="ID")
    is_active: bool = Field(title="회원 상태", description="회원 상태")
    items: list[ItemResponseSchema] = []

    class Config:
        from_attributes = True
