from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from models.study_session import SessionState
from schemas.study_plan_schemas import StudyPlanMinimalResponse, StudyPlanTopicResponse


class StudySessionStart(BaseModel):
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


class StudySessionResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None
    topics: Optional[List[StudyPlanTopicResponse]] = None
    plan: StudyPlanMinimalResponse

    last_pause_time: Optional[datetime] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_pause_time: Optional[float] = None
    status: SessionState


class StudyTimeByCourseResponse(BaseModel):
    course: str
    time: float


class StudySessionUpdate(BaseModel):
    notes: str
    topics: List[UUID]
