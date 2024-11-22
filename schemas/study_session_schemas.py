import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from schemas.study_plan_schemas import StudyPlanTopicResponse


class StudySessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None

    plan_id: uuid.UUID
    topics: List[StudyPlanTopicResponse]

    started_at: datetime
    ended_at: Optional[datetime] = None
    total_pause_time: Optional[float] = 0.0


class StudySessionCreateUpdate(StudySessionBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "Algebra Study Session",
                "description": "Focused session to cover Algebra basics",
                "plan_id": "550e8400-e29b-41d4-a716-446655440000",
                "started_at": "2024-11-20T09:00:00Z",
                "topics": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655441111",
                        "title": "Geometry Fundamentals",
                        "created_at": "2024-11-20T09:00:00Z"
                    }
                ]
            }
        }


class StudySessionResponse(StudySessionBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
