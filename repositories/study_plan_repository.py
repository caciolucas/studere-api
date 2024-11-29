from typing import List, Optional
from uuid import UUID

from core.exceptions import DatabaseError
from core.repository import BaseRepository
from models.course import Course
from models.study_plan import StudyPlan, StudyPlanTopic
from models.term import Term


class StudyPlanRepository(BaseRepository):
    def create_study_plan(self, study_plan: StudyPlan) -> StudyPlan:
        try:
            self.db.add(study_plan)
            self.db.commit()
            self.db.refresh(study_plan)
            return study_plan
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def retrieve_study_plan(self, study_plan_id: UUID) -> StudyPlan:
        try:
            return (
                self.db.query(StudyPlan).filter(StudyPlan.id == study_plan_id).first()
            )
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def retrieve_study_topic(self, study_topic_id: UUID) -> StudyPlanTopic:
        try:
            return (
                self.db.query(StudyPlanTopic)
                .filter(StudyPlanTopic.id == study_topic_id)
                .first()
            )
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def update_study_plan(self, study_plan: StudyPlan) -> StudyPlan:
        try:
            self.db.merge(study_plan)
            self.db.commit()
            self.db.refresh(study_plan)
            return study_plan
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def delete_study_plan(self, study_plan_id: UUID) -> None:
        try:
            study_plan = (
                self.db.query(StudyPlan).filter(StudyPlan.id == study_plan_id).first()
            )
            self.db.delete(study_plan)
            self.db.commit()
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def list_study_plans(
        self, user_id: Optional[UUID] = None, course_id: Optional[UUID] = None
    ) -> list[StudyPlan]:
        try:
            if course_id:
                return (
                    self.db.query(StudyPlan)
                    .filter(StudyPlan.course_id == course_id)
                    .all()
                )

            if user_id:
                return (
                    self.db.query(StudyPlan)
                    .join(Course)
                    .join(Term)
                    .filter(Term.user_id == user_id)
                    .all()
                )
            return self.db.query(StudyPlan).all()
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def create_study_plan_topics(
        self, topics: List[StudyPlanTopic]
    ) -> List[StudyPlanTopic]:
        try:
            self.db.add_all(topics)
            self.db.commit()
            for topic in topics:
                self.db.refresh(topic)
            return topics
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e

    def delete_study_plan_topics(self, topics_ids: List[str]) -> None:
        try:
            topics = (
                self.db.query(StudyPlanTopic)
                .filter(StudyPlanTopic.id.in_(topics_ids))
                .all()
            )
            for topic in topics:
                self.db.delete(topic)
            self.db.commit()
        except Exception as e:
            raise DatabaseError(
                f"Operation failed due to internal database error:\n{e}"
            ) from e
