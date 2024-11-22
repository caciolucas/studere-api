import json
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqalchemy.orm import Session

from core.service import BaseService
from models.study_session import StudySession
from repositories.study_session_repository import StudySessionRepository
from schemas.study_session_schemas import StudySessionCreateUpdate, StudySessionResponse
from schemas.study_plan_schemas import StudyPlanTopicResponse
from services.study_plan_service import StudyPlanService


class StudySessionService(BaseService):
    def __init__(self, db: Session):
        self.repository = StudySessionRepository(db)
        self.study_plan_service = StudyPlanService(db)

    def create_study_session(
        self,
        title: str,
        plan_id: str,
        topics: List[StudyPlanTopicResponse],

        description: Optional[str] = None,
        notes: Optional[str] = None,
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        total_pause_time: Optional[float] = 0.0
    ) -> StudySession:
        study_session_model = StudySession(
            title=title,
            plan_id=plan_id,
            topics=topics,
            description=description,
            notes=notes,
            started_at=started_at if started_at else datetime.now(),
            ended_at=ended_at,
            total_pause_time=total_pause_time
        )

        new_study_session = StudySession(study_session_model)
        return self.repository.create_study_session(new_study_session)

    # TODO: PAUSE AND UNPAUSE, LIST AND SUCH
