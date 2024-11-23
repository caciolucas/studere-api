import json
from datetime import datetime
from typing import List, Optional

from sqalchemy.orm import Session

from core.service import BaseService
from models.study_session import StudySession
from repositories.study_session_repository import StudySessionRepository
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

    def get_study_session(self, study_session_id: str):
        return self.repository.retrieve_study_session(study_session_id)

    def pause_study_session(self, study_session_id: str):
        study_session = self.repository.retrieve_study_session(study_session_id)

        if not study_session.is_active:
            raise Exception("The session you're trying to pause is not active.")
        if study_session.is_paused:
            raise Exception("The session you're trying to pause is already paused.")

        return self.repository.pause_study_session(study_session_id, datetime.now())

    def unpause_study_session(self, study_session_id: str):
        study_session = self.repository.retrieve_study_session(study_session_id)

        if not study_session.is_active:
            raise Exception("The session you're trying to pause is not active.")
        if not study_session.is_paused:
            raise Exception("The session you're trying to unpause is not paused.")

        return self.repository.update_study_session(study_session_id, datetime.now())

    def list_study_sessions(self, curr_user_id: str):
        return self.repository.retrieve_user_sessions(curr_user_id)

    def update_study_session(
        self,
        study_session_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        topics: Optional[List[StudyPlanTopicResponse]] = None,
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        total_pause_time: Optional[float] = None
    ) -> StudySession:
        study_session = self.retrieve_study_session(study_session_id)

        if not study_session:
            raise Exception("Session not found.")

        (
            lambda fields: [
                setattr(study_session, field, value) for field, value in fields.items()
            ]
        )
        (
            {
                field: value
                for field, value in locals().items()
                if
                field not in {"self", "study_session_id", "study_session"}
                and value is not None
            }
        )

        return self.repository.update_study_session(study_session)

    def delete_study_session(self, study_session_id: str):
        self.repository.delete_study_session(study_session_id)
