from uuid import UUID
from sqlalchemy.sql import func
from typing import List
from datetime import date, timedelta

from core.exceptions import RepositoryError
from core.repository import BaseRepository

from models.course import Course
from models.study_plan import StudyPlan
from models.study_session import StudySession
from models.term import Term


class DashboardRepository(BaseRepository):
    def get_study_time_by_course(self, curr_user_id: UUID) -> List[dict]:
        try:
            results = (
                self.db.query(
                    Course.name,
                    func.sum(
                        func.extract(
                            "epoch", StudySession.ended_at - StudySession.started_at
                        ) - StudySession.total_pause_time
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

    def get_study_sessions_last_7_days(self, curr_user_id: UUID) -> List[dict]:
        try:
            today = date.today()
            seven_days_ago = today - timedelta(days=6)

            results = (
                self.db.query(
                    func.date(StudySession.started_at).label("study_date"),
                    func.count(StudySession.id).label("session_count"),
                )
                .join(StudyPlan, StudySession.plan_id == StudyPlan.id)
                .join(Course, StudyPlan.course_id == Course.id)
                .join(Term, Course.term_id == Term.id)
                .filter(Term.user_id == curr_user_id)
                .filter(StudySession.started_at >= seven_days_ago)
                .filter(StudySession.started_at <= today)
                .group_by(func.date(StudySession.started_at))
                .order_by(func.date(StudySession.started_at))
                .all()
            )

            return [{"study_date": row.study_date, "session_count": row.session_count} for row in results]
        except Exception as e:
            raise RepositoryError(f"Failed to fetch study sessions in the last 7 days: {e}") from e

    def get_time_distribution(self, curr_user_id: UUID) -> List[dict]:
        try:
            results = (
                self.db.query(
                    func.to_char(StudySession.started_at, "Day").label("day_of_week"),
                    func.sum(
                        func.extract("epoch", StudySession.ended_at - StudySession.started_at) - StudySession.total_pause_time
                    ).label("total_time"),
                )
                .join(StudyPlan, StudySession.plan_id == StudyPlan.id)
                .join(Course, StudyPlan.course_id == Course.id)
                .join(Term, Course.term_id == Term.id)
                .filter(Term.user_id == curr_user_id)
                .group_by(func.to_char(StudySession.started_at, "Day"), StudySession.started_at)
                .order_by(func.to_char(StudySession.started_at, "D"))
                .all()
            )

            return [{"name": row.day_of_week.strip(), "time": row.total_time} for row in results]
        except Exception as e:
            raise RepositoryError(f"Failed to fetch time distribution: {e}") from e
