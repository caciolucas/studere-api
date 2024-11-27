from typing import Optional
from uuid import UUID

from core.exceptions import DatabaseError
from core.repository import BaseRepository
from models.study_session import SessionState, StudySession


class StudySessionRepository(BaseRepository):
    def save_study_session(self, study_session: StudySession) -> StudySession:
        try:
            self.db.add(study_session)
            self.db.commit()
            self.db.refresh(study_session)

            return study_session

        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def retrieve_current_study_session_for_plan_id(
        self, plan_id: UUID
    ) -> Optional[StudySession]:
        try:
            return (
                self.db.query(StudySession)
                .filter(
                    StudySession.plan_id == plan_id,
                    StudySession.status.in_(
                        [SessionState.ACTIVE.value, SessionState.PAUSED.value]
                    ),
                )
                .first()
            )

        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def list_plan_sessions(self, plan_id: UUID) -> Optional[StudySession]:
        try:
            return (
                self.db.query(StudySession)
                .filter(StudySession.plan_id == plan_id)
                .all()
            )

        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e
