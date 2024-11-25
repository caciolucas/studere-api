from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import (
    NotFoundError,
    PauseInactiveSessionError,
    SessionAlreadyPausedError,
    SessionNotPausedError,
)
from core.service import BaseService
from models.study_session import StudySession
from repositories.study_session_repository import StudySessionRepository
from services.study_plan_service import StudyPlanService


class StudySessionService(BaseService):
    def __init__(self, db: Session):
        self.repository = StudySessionRepository(db)
        self.study_plan_service = StudyPlanService(db)

    def create_study_session(
        self,
        title: str,
        plan_id: UUID,
        topics: Optional[List[UUID]],
        description: Optional[str] = None,
        notes: Optional[str] = None,
        started_at: Optional[datetime] = datetime.now(),
        ended_at: Optional[datetime] = None,
        total_pause_time: Optional[float] = 0.0,
    ) -> StudySession:
        if ended_at and started_at > ended_at:
            raise ValueError("The start time cannot be greater than the end time.")

        new_study_session = StudySession(
            title=title,
            plan_id=plan_id,
            description=description,
            notes=notes,
            started_at=started_at,
            ended_at=ended_at,
            total_pause_time=total_pause_time,
        )

        retrieved_topics = [
            self.study_plan_service.retrieve_study_topic(topic_id)
            for topic_id in topics
        ]
        new_study_session.topics = retrieved_topics

        return self.repository.create_study_session(new_study_session)

    def get_study_session(self, study_session_id: str):
        study_session = self.repository.retrieve_study_session(study_session_id)
        if study_session is None:
            raise NotFoundError(f"Study session not found: {study_session_id}")
        return study_session

    def pause_study_session(self, study_session_id: str):
        study_session = self.get_study_session(study_session_id)

        if not study_session.is_active:
            raise PauseInactiveSessionError(
                "The session you're trying to pause is not active."
            )
        if study_session.is_paused:
            raise SessionAlreadyPausedError(
                "The session you're trying to pause is already paused."
            )

        return self.repository.pause_study_session(study_session_id, datetime.now())

    def unpause_study_session(self, study_session_id: str):
        study_session = self.get_study_session(study_session_id)

        if not study_session.is_active:
            raise PauseInactiveSessionError(
                "The session you're trying to pause is not active."
            )
        if not study_session.is_paused:
            raise SessionNotPausedError(
                "The session you're trying to unpause is not paused."
            )

        elapsed_time = (
            (datetime.now() - study_session.last_pause_time).total_seconds()
            if study_session.last_pause_time
            else 0.0
        )

        return self.repository.unpause_study_session(study_session_id, elapsed_time)

    def list_study_sessions(self, curr_user_id: UUID):
        return self.repository.retrieve_user_sessions(curr_user_id)

    def update_study_session(
        self,
        study_session_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        topics: Optional[List[UUID]] = None,
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        total_pause_time: Optional[float] = None,
    ) -> StudySession:
        if started_at and ended_at and started_at > ended_at:
            raise ValueError("The start time cannot be greater than the end time.")

        study_session = self.get_study_session(study_session_id)

        topics = (
            [
                self.study_plan_service.retrieve_study_topic(topic_id)
                for topic_id in topics
            ]
            if topics
            else None
        )

        (
            lambda fields: [
                setattr(study_session, field, value) for field, value in fields.items()
            ]
        )(
            {
                field: value
                for field, value in locals().items()
                if field not in {"self", "study_session_id", "study_session"}
                and value is not None
            }
        )

        return self.repository.update_study_session(study_session)

    def delete_study_session(self, study_session_id: str):
        # try to get it first, so if it doesnt exist
        self.get_study_session(study_session_id)
        self.repository.delete_study_session(study_session_id)
