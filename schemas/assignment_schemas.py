import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssignmentCreateUpdate(BaseModel):
    course_id: uuid.UUID
    title: str
    type: str
    description: Optional[str] = None
    score: Optional[int] = 0
    due_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Final Exam",
                "type": "exam",
                "description": "Final assessment for the course.",
                "score": 100,
                "due_at": "2024-12-15T23:59:59",
            }
        }


class AssignmentPartialUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    score: Optional[int] = None
    due_at: Optional[datetime] = None
    course_id: Optional[uuid.UUID] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Project",
                "type": "project",
                "description": "Updated description for the assignment.",
                "score": 85,
                "due_at": "2024-12-10T23:59:59",
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }


class AssignmentResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    type: str
    description: Optional[str] = None
    score: Optional[int] = None
    due_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Final Exam",
                "type": "exam",
                "description": "Final assessment for the course.",
                "score": 100,
                "due_at": "2024-12-15T23:59:59",
                "created_at": "2024-11-07T12:00:00",
            }
        }
