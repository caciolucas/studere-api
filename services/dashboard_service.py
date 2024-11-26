from typing import List
from uuid import UUID
from datetime import date, timedelta

from sqlalchemy.orm import Session

from core.exceptions import (
    NotFoundError,
)
from core.service import BaseService

from repositories.dashboard_repository import DashboardRepository


class DashboardService(BaseService):
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_study_time_by_course(self, curr_user_id: UUID) -> List[dict]:
        study_time = self.repository.get_study_time_by_course(curr_user_id)
        if study_time is None:
            raise NotFoundError(f"No study time data found for user {curr_user_id}")
        return study_time

    def get_study_streaks(self, curr_user_id: UUID) -> List[dict]:
        study_dates = self.repository.get_study_sessions_last_7_days(curr_user_id)
        if study_dates is None:
            raise NotFoundError(f"No study sessions found for user {curr_user_id} in the last 7 days")

        today = date.today()
        last_7_days = [today - timedelta(days=i) for i in range(7)][::-1]

        study_date_set = {session["study_date"] for session in study_dates}

        return [day in study_date_set for day in last_7_days]

    def get_time_distribution(self, curr_user_id: UUID) -> List[dict]:
        raw_data = self.repository.get_time_distribution(curr_user_id)

        if raw_data is None:
            raise NotFoundError(f"No time distribution data found for user {curr_user_id}")

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        formatted_data = [
            {"name": day, "time": next((d["time"] for d in raw_data if d["name"].startswith(day)), 0)}
            for day in days_of_week
        ]

        return formatted_data
