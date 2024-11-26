import json
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.constants import DEFAULT_PROMPT, OPEN_AI_KEY
from core.exceptions import NotFoundError, OpenAIInvalidFormatError
from core.service import BaseService
from models.study_plan import StudyPlan, StudyPlanTopic
from repositories.study_plan_repository import StudyPlanRepository
from schemas.study_plan_schemas import StudyPlanTopicCreateUpdate
from services.course_service import CourseService
from services.openai_service import OpenAIService


class StudyPlanService(BaseService):
    def __init__(self, db: Session):
        self.repository = StudyPlanRepository(db)
        self.course_service = CourseService(db)
        self.openai_service = OpenAIService(OPEN_AI_KEY)

    def create_study_plan(
        self,
        title: str,
        course_id: UUID,
        current_user_id: UUID,
        topics: List[StudyPlanTopicCreateUpdate],
    ) -> StudyPlan:
        course = self.course_service.retrieve_course(course_id, current_user_id)
        study_plan = StudyPlan(title=title, course=course)
        plan = self.repository.create_study_plan(study_plan)
        topics_objects: List[StudyPlanTopic] = [
            StudyPlanTopic(
                title=topic.title,
                description=topic.description,
                completed_at=None,
                plan_id=plan.id,
            )
            for topic in topics
        ]
        self.repository.create_study_plan_topics(topics_objects)
        self.repository.db.refresh(plan)
        return plan

    def list_study_plans(self, user_id: UUID, course_id: Optional[UUID] = None):
        if course_id:
            self.course_service.retrieve_course(course_id, user_id)
        return self.repository.list_study_plans(user_id, course_id)

    def retrieve_study_topic(self, study_topic_id: str):
        study_topic = self.repository.retrieve_study_topic(study_topic_id)
        if not study_topic:
            raise NotFoundError(f"Study topic not found: {study_topic_id}")
        return study_topic

    def retrieve_study_plan(self, study_plan_id: UUID, current_user_id: UUID):
        study_plan = self.repository.retrieve_study_plan(study_plan_id)
        if not study_plan or study_plan.course.term.user_id != current_user_id:
            raise NotFoundError(f"Study plan not found: {study_plan_id} (user: {current_user_id})")
        return study_plan

    def update_study_plan(
        self,
        study_plan_id: UUID,
        current_user_id: UUID,
        course_id: Optional[UUID] = None,
        title: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
        score: Optional[int] = None,
    ):
        study_plan = self.retrieve_study_plan(study_plan_id, current_user_id)

        if course_id:
            study_plan.course_id = course_id
        if title:
            study_plan.title = title
        if type:
            study_plan.type = type
        if description:
            study_plan.description = description
        if due_at:
            study_plan.due_at = due_at
        if score is not None:
            study_plan.score = score

        return self.repository.update_study_plan(study_plan)

    def delete_study_plan(self, study_plan_id: UUID, current_user_id: UUID):
        self.retrieve_study_plan(study_plan_id, current_user_id)
        return self.repository.delete_study_plan(study_plan_id)

    def ai_generate_study_plan(
        self, prompt: str, course_id: UUID, current_user_id: UUID
    ):
        course = self.course_service.retrieve_course(course_id, current_user_id)
        response = self.openai_service.get_response(DEFAULT_PROMPT.format(prompt))

        try:
            json_content = json.loads(response)
        except Exception as e:
            raise OpenAIInvalidFormatError(f"Invalid OpenAI response format: {e}") from e

        if isinstance(json_content, list):
            json_content = json_content[0]

        course = self.repository.db.merge(course)
        study_plan = StudyPlan(title=json_content["title"], course=course)
        study_plan = self.repository.create_study_plan(study_plan)

        topics = [
            StudyPlanTopic(
                title=topic["title"], description=topic["description"], plan=study_plan
            )
            for topic in json_content["topics"]
        ]

        topics = self.repository.create_study_plan_topics(topics)
        self.repository.db.refresh(study_plan)
        return study_plan
