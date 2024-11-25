from datetime import datetime
from typing import List
from uuid import UUID

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.course import Course
from models.study_plan import StudyPlan
from models.study_session import StudySession


class StudySessionRepository(BaseRepository):
    def create_study_session(self, study_session: StudySession) -> StudySession:
        try:
            self.db.add(study_session)
            self.db.commit()
            self.db.refresh(study_session)
            return study_session
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def update_study_session(self, study_session: StudySession) -> StudySession:
        try:
            self.db.merge(study_session)
            self.db.commit()
            self.db.refresh(study_session)
            return study_session
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def retrieve_study_session(self, study_session_id: str) -> StudySession:
        try:
            return (
                self.db.query(StudySession)
                .filter(StudySession.id == study_session_id)
                .first()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def delete_study_session(self, study_session_id: str) -> None:
        try:
            study_session = (
                self.db.query(StudySession)
                .filter(StudySession.id == study_session_id)
                .first()
            )

            self.db.delete(study_session)
            self.db.commit()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def list_study_session(self, plan_id: str) -> List[StudySession]:
        try:
            return (
                self.db.query(StudySession)
                .filter(StudySession.plan_id == plan_id)
                .all()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def pause_study_session(
        self, study_session_id: str, pause_start: datetime
    ) -> StudySession:
        try:
            study_session = (
                self.db.query(StudySession)
                .filter(StudySession.id == study_session_id)
                .first()
            )

            study_session.is_paused = True
            study_session.last_pause_time = pause_start

            self.db.commit()
            self.db.refresh(study_session)
            return study_session
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def unpause_study_session(
        self, study_session_id: str, elapsed_time: float
    ) -> StudySession:
        try:
            study_session = (
                self.db.query(StudySession)
                .filter(StudySession.id == study_session_id)
                .first()
            )

            study_session.is_paused = False
            study_session.last_pause_time = None
            study_session.total_pause_time += elapsed_time

            self.db.commit()
            self.db.refresh(study_session)
            return study_session
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def retrieve_user_sessions(self, curr_user_id: UUID):
        try:
            return (
                self.db.query(StudySession)
                .join(StudyPlan, StudySession.plan_id == StudyPlan.id)
                .join(Course, StudyPlan.course_id == Course.id)
                .filter(Course.user_id == curr_user_id)
                .all()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e
