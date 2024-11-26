from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.study_plan_schemas import StudyPlanMinimalResponse, StudyPlanTopicResponse


class StudySessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None
    topics: Optional[List[UUID]] = None

    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    total_pause_time: Optional[float] = None

    is_active: Optional[bool] = None


class StudySessionCreate(StudySessionBase):
    plan_id: UUID

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
                        "created_at": "2024-11-20T09:00:00Z",
                    }
                ],
            }
        }


class StudySessionUpdate(StudySessionBase):
    title: Optional[str] = None

    class Config:
        fields = {"is_active": {"exclude": True}}


class StudySessionResponse(StudySessionBase):
    id: UUID
    topics: Optional[List[StudyPlanTopicResponse]] = None
    plan: StudyPlanMinimalResponse
    last_pause_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudyTimeByCourseResponse(BaseModel):
    course: str
    time: float
