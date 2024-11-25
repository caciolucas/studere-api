import uuid

from pydantic import BaseModel
from datetime import date


class TermCreateUpdate(BaseModel):
    name: str
    start_date: date
    end_date: date


class TermResponse(BaseModel):
    id: uuid.UUID
    name: str
    user_id: uuid.UUID

    start_date: date
    end_date: date

    class Config:
        from_attibutes = True
