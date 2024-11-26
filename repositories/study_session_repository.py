from datetime import datetime
from typing import List
from uuid import UUID

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.course import Course
from models.study_plan import StudyPlan
from models.study_session import StudySession
from models.term import Term
from sqlalchemy.sql import func


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

    def end_study_session(
        self, study_session_id: str, pause_start: datetime
    ) -> StudySession:
        try:
            study_session = (
                self.db.query(StudySession)
                .filter(StudySession.id == study_session_id)
                .first()
            )

            study_session.is_active = False
            study_session.ended_at = datetime.now()
            self.db.commit()
            self.db.refresh(study_session)
            return study_session
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
                .join(Term, Course.term_id == Term.id)
                .filter(Term.user_id == curr_user_id)
                .all()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def get_study_time_by_course(self, curr_user_id: UUID) -> List[dict]:
        try:
            results = (
                self.db.query(
                    Course.name,
                    func.sum(
                        func.extract(
                            "epoch", StudySession.ended_at - StudySession.started_at
                        )
                        - StudySession.total_pause_time
                    ).label("time"),
                )
                .join(StudyPlan, StudySession.plan_id == StudyPlan.id)
                .join(Course, StudyPlan.course_id == Course.id)
                .join(Term, Course.term_id == Term.id)
                .filter(Term.user_id == curr_user_id)
                .group_by(Course.name)
                .all()
            )
            return [{"course": row[0], "time": row[1]} for row in results]

        except Exception as e:
            raise RepositoryError(f"Failed to fetch study time by course: {e}") from e
