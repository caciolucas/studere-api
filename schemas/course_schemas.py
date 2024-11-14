import uuid

from pydantic import BaseModel


class CourseCreateUpdate(BaseModel):
    name: str


class CourseResponse(BaseModel):
    id: uuid.UUID
    name: str
    user_id: uuid.UUID

    class Config:
        from_attibutes = True
