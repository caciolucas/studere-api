from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.service import BaseService
from models.course import Course
from repositories.course_repository import CourseRepository
from services.user_service import UserService


class CourseService(BaseService):
    def __init__(self, db: Session):
        self.repository = CourseRepository(db)
        self.user_service = UserService(db)

    def create_course(self, name: str, user_id: str):
        user = self.user_service.retrieve_user(user_id)
        new_task = Course(name=name, user_id=user.id)

        return self.repository.create_course(new_task)

    def list_courses(self, user_id: Optional[str] = None):
        return self.repository.list_courses(user_id)

    def retrieve_course(self, course_id: str, current_user_id: str):
        course = self.repository.retrieve_course(course_id)
        if not course or course.user_id != current_user_id:
            raise HTTPException(status_code=404, detail="Course not found")

        return course

    def update_course(
        self,
        course_id: str,
        name: Optional[str] = None,
        current_user_id: Optional[str] = None,
    ):
        course = self.retrieve_course(course_id, current_user_id)
        if name:
            course.name = name

        return self.repository.update_course(course)

    def delete_course(self, course_id: str, current_user_id: str):
        course = self.retrieve_course(course_id, current_user_id)
        return self.repository.delete_course(course.id)
