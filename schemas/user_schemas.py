from uuid import UUID
from datetime import date

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    created_at: date

    class Config:
        # This allows automatic conversion from a SQLAlchemy model to Pydantic
        from_attibutes = True


class UserLoginResponse(UserLogin):
    access_token: str
    token_type: str
