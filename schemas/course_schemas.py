from uuid import UUID
from pydantic import BaseModel

from schemas.term_schemas import TermResponse


class CourseCreateUpdate(BaseModel):
    name: str
    term_id: UUID


class CourseResponse(BaseModel):
    id: UUID
    name: str
    term: TermResponse

    class Config:
        from_attibutes = True
