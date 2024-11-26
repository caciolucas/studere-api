from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import (
    ActiveSessionExistsError,
    NotFoundError,
    PauseInactiveSessionError,
    SessionAlreadyFinishedError,
    SessionNotPausedError,
)
from core.service import BaseService
from models.study_session import SessionState, StudySession
from repositories.study_session_repository import StudySessionRepository
from services.study_plan_service import StudyPlanService


class StudySessionService(BaseService):
    def __init__(self, db: Session):
        self.repository = StudySessionRepository(db)
        self.study_plan_service = StudyPlanService(db)

    def start_study_session(
        self,
        title: str,
        plan_id: UUID,
        description: Optional[str] = None,
    ) -> StudySession:
        active_study_session = (
            self.repository.retrieve_current_study_session_for_plan_id(plan_id)
        )

        if active_study_session:
            raise ActiveSessionExistsError(
                "An active session already exists for this plan."
            )

        new_study_session = StudySession(
            title=title,
            plan_id=plan_id,
            description=description,
        )

        return self.repository.save_study_session(new_study_session)

    def retrieve_current_study_session_for_plan_id(self, plan_id: str):
        study_session = self.repository.retrieve_current_study_session_for_plan_id(
            plan_id
        )
        if study_session is None:
            raise NotFoundError(f"Study session not found: {plan_id}")
        return study_session

    def end_study_session(self, plan_id: UUID):
        study_session = self.repository.retrieve_current_study_session_for_plan_id(
            plan_id
        )
        if study_session.status == SessionState.COMPLETED.value:
            raise SessionAlreadyFinishedError(
                "The session you're trying to end is not active."
            )

        if study_session.status == SessionState.PAUSED.value:
            self.unpause_study_session(study_session.id)

        study_session.status = SessionState.COMPLETED.value
        study_session.ended_at = datetime.now()
        study_session.study_time = study_session.ended_at - study_session.started_at
        study_session.study_time -= timedelta(seconds=study_session.total_pause_time)
        study_session.study_time = study_session.study_time.total_seconds()

        return self.repository.save_study_session(study_session)

    def unpause_study_session(self, plan_id: UUID):
        study_session = self.repository.retrieve_current_study_session_for_plan_id(
            plan_id
        )
        if study_session.status != SessionState.PAUSED.value:
            raise SessionNotPausedError(
                "The session you're trying to unpause is not paused."
            )

        pause_elapsed_time = (
            (datetime.now() - study_session.last_pause_time).total_seconds()
            if study_session.last_pause_time
            else 0.0
        )
        study_session.total_pause_time += pause_elapsed_time
        study_session.last_pause_time = None
        study_session.status = SessionState.ACTIVE.value

        return self.repository.save_study_session(study_session)

    def pause_study_session(self, study_session_id: str):
        study_session = self.repository.retrieve_current_study_session_for_plan_id(
            study_session_id
        )

        if study_session.status != SessionState.ACTIVE.value:
            raise PauseInactiveSessionError(
                "The session you're trying to pause is not active."
            )

        study_session.status = SessionState.PAUSED.value
        study_session.last_pause_time = datetime.now()

        return self.repository.save_study_session(study_session)

    def list_session_plan_history(self, plan_id: UUID):
        return self.repository.list_plan_sessions(plan_id)