import uuid

from pydantic import BaseModel


class CourseCreateUpdate(BaseModel):
    name: str
    term_id: uuid.UUID


class CourseResponse(BaseModel):
    id: uuid.UUID
    name: str
    term_id: uuid.UUID

    class Config:
        from_attibutes = True
