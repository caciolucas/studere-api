from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from core.service import BaseService
from models.course import Course
from repositories.course_repository import CourseRepository
from services.user_service import UserService
from services.term_service import TermService


class CourseService(BaseService):
    def __init__(self, db: Session):
        self.repository = CourseRepository(db)
        self.user_service = UserService(db)
        self.term_service = TermService(db)

    def create_course(self, name: str, term_id: UUID):
        course = Course(name=name, term_id=term_id)
        return self.repository.create_course(course)

    def list_courses(self, user_id: UUID, term_id: Optional[UUID] = None):
        if term_id:
            self.term_service.retrieve_term(term_id, user_id)
        return self.repository.list_courses(user_id, term_id)

    def retrieve_course(self, course_id: UUID, current_user_id: UUID):
        course = self.repository.retrieve_course(course_id)
        if not course or course.term.user_id != current_user_id:
            raise NotFoundError(
                f"Course not found: {course_id} (user: {current_user_id})"
            )
        return course

    def update_course(
        self,
        course_id: UUID,
        current_user_id: UUID,
        name: Optional[str] = None,
    ):
        course = self.retrieve_course(course_id, current_user_id)

        if name:
            course.name = name

        return self.repository.update_course(course)

    def delete_course(self, course_id: UUID, current_user_id: UUID):
        self.retrieve_course(course_id, current_user_id)
        return self.repository.delete_course(course_id)
