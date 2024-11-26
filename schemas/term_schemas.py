import uuid
from datetime import date, datetime

from pydantic import BaseModel


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
    created_at: datetime

    class Config:
        from_attibutes = True
