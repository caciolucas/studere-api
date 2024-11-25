from typing import List, Optional

from uuid import UUID
from core.repository import BaseRepository
from models.course import Course
from models.study_plan import StudyPlan, StudyPlanTopic
from models.term import Term


class StudyPlanRepository(BaseRepository):
    def create_study_plan(self, study_plan: StudyPlan) -> StudyPlan:
        self.db.add(study_plan)
        self.db.commit()
        self.db.refresh(study_plan)
        return study_plan

    def retrieve_study_plan(self, study_plan_id: UUID) -> StudyPlan:
        return self.db.query(StudyPlan).filter(StudyPlan.id == study_plan_id).first()

    def retrieve_study_topic(self, study_topic_id: str) -> StudyPlanTopic:
        return (
            self.db.query(StudyPlanTopic)
            .filter(StudyPlanTopic.id == study_topic_id)
            .first()
        )

    def update_study_plan(self, study_plan: StudyPlan) -> StudyPlan:
        self.db.merge(study_plan)
        self.db.commit()
        self.db.refresh(study_plan)
        return study_plan

    def delete_study_plan(self, study_plan_id: UUID) -> None:
        study_plan = (
            self.db.query(StudyPlan).filter(StudyPlan.id == study_plan_id).first()
        )
        if study_plan:
            self.db.delete(study_plan)
            self.db.commit()

    def list_study_plans(
        self, user_id: Optional[UUID] = None, course_id: Optional[UUID] = None
    ) -> list[StudyPlan]:
        if course_id:
            return (
                self.db.query(StudyPlan).filter(StudyPlan.course_id == course_id).all()
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

    def create_study_plan_topics(
        self, topics: List[StudyPlanTopic]
    ) -> List[StudyPlanTopic]:
        self.db.add_all(topics)
        self.db.commit()
        for topic in topics:
            self.db.refresh(topic)
        return topics

    def delete_study_plan_topics(self, topics_ids: List[str]) -> None:
        topics = (
            self.db.query(StudyPlanTopic)
            .filter(StudyPlanTopic.id.in_(topics_ids))
            .all()
        )
        for topic in topics:
            self.db.delete(topic)
        self.db.commit()
