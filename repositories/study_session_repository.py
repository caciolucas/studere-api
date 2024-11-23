from typing import List
from datetime import datetime

from core.repository import BaseRepository
from models.study_session import StudySession
from models.study_plan import StudyPlan
from models.course import Course


class StudySessionRepository(BaseRepository):
    def create_study_session(self, study_session: StudySession) -> StudySession:
        self.db.add(study_session)
        self.db.commit()
        self.db.refresh(study_session)
        return study_session

    def update_study_session(self, study_session: StudySession) -> StudySession:
        self.db.merge(study_session)
        self.db.commit()
        self.db.refresh(study_session)
        return study_session

    def retrieve_study_session(self, study_session_id: str) -> StudySession:
        return self.db.query(StudySession).filter(StudySession.id == study_session_id).first()

    def delete_study_session(self, study_session_id: str) -> None:
        study_session = (
            self.db.query(StudySession).filter(StudySession.id == study_session_id).first()
        )

        # should this verification be really done?
        if not study_session:
            raise ValueError("Study session not found!")

        self.db.delete(study_session)
        self.db.commit()

    def list_study_session(self, plan_id: str) -> List[StudySession]:
        return self.db.query(StudySession).filter(StudySession.plan_id == plan_id).all()

    def pause_study_session(self, study_session_id: str, pause_start: datetime) -> StudySession:
        study_session = (
            self.db.query(StudySession).filter(StudySession.id == study_session_id).first()
        )

        if not study_session:
            raise ValueError("Study session not found!")

        study_session.is_paused = True
        study_session.last_pause_time = pause_start

        self.db.commit()
        self.db.refresh(study_session)
        return study_session

    def end_pause(self, study_session_id: str, unpause_time: datetime) -> StudySession:
        study_session = (
            self.db.query(StudySession).filter(StudySession.id == study_session_id).first()
        )

        if not study_session:
            raise ValueError("Study session not found!")

        elapsed_time = (
            (unpause_time - study_session.last_pause_time).total_seconds()
            if study_session.last_pause_time
            else 0.0
        )

        study_session.is_paused = False
        study_session.last_pause_time = None
        study_session.total_pause_time += elapsed_time

        self.db.commit()
        self.db.refresh(study_session)
        return study_session

    def retrieve_user_sessions(self, curr_user_id: str):
        return (
            self.db.query(StudySession)
            .join(StudyPlan, StudySession.plan_id == StudyPlan.id)
            .join(Course, StudyPlan.course_id == Course.id)
            .filter(Course.user_id == curr_user_id)
            .all()
        )
