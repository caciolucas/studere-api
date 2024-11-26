from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.study_plan_schemas import StudyPlanMinimalResponse, StudyPlanTopicResponse


class StudySessionCreate(BaseModel):
    title: str
    description: str
    plan_id: UUID

    class Config:
        schema_extra = {
            "example": {
                "title": "Algebra Study Session",
                "description": "Focused session to cover Algebra basics",
                "plan_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }


class StudySessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None

    started_at: datetime
    ended_at: Optional[datetime] = None
    total_pause_time: Optional[float] = None

    is_active: Optional[bool] = None


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
