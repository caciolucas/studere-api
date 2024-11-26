from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from core.service import BaseService
from models.assignment import Assignment, AssignmentType
from repositories.assignment_repository import AssignmentRepository
from services.course_service import CourseService


class AssignmentService(BaseService):
    def __init__(self, db: Session):
        self.repository = AssignmentRepository(db)
        self.course_service = CourseService(db)

    def create_assignment(
        self,
        title: str,
        type: AssignmentType,
        description: Optional[str],
        course_id: UUID,
        current_user_id: UUID,
        due_at: datetime,
        score: Optional[int] = 0,
    ) -> Assignment:
        course = self.course_service.retrieve_course(course_id, current_user_id)

        new_assignment = Assignment(
            title=title,
            type=type.value,
            description=description,
            course=course,
            due_at=due_at,
            score=score,
        )
        return self.repository.create_assignment(new_assignment)

    def list_assignments(self, user_id: UUID, course_id: Optional[UUID] = None):
        if course_id:
            self.course_service.retrieve_course(course_id, user_id)
        return self.repository.list_assignments(user_id, course_id)

    def retrieve_assignment(self, assignment_id: UUID, current_user_id: UUID):
        assignment = self.repository.retrieve_assignment(assignment_id)
        if not assignment or assignment.course.user_id != current_user_id:
            raise NotFoundError(
                f"Assigment not found: {assignment_id} (user: {current_user_id})"
            )
        return assignment

    def update_assignment(
        self,
        assignment_id: UUID,
        current_user_id: UUID,
        course_id: Optional[UUID] = None,
        title: Optional[str] = None,
        type: Optional[AssignmentType] = None,
        description: Optional[str] = None,
        due_at: Optional[datetime] = None,
        score: Optional[int] = None,
    ):
        assignment = self.retrieve_assignment(assignment_id, current_user_id)

        if course_id:
            assignment.course_id = course_id
        if title:
            assignment.title = title
        if type:
            assignment.type = type
        if description:
            assignment.description = description
        if due_at:
            assignment.due_at = due_at
        if score is not None:
            assignment.score = score

        return self.repository.update_assignment(assignment)

    def delete_assignment(self, assignment_id: UUID, current_user_id: UUID):
        self.retrieve_assignment(assignment_id, current_user_id)
        return self.repository.delete_assignment(assignment_id)
