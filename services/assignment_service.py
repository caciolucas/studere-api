from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.service import BaseService
from models.assignment import Assignment
from repositories.assignment_repository import AssignmentRepository
from services.course_service import CourseService


class AssignmentService(BaseService):
    def __init__(self, db: Session):
        self.repository = AssignmentRepository(db)
        self.course_service = CourseService(db)

    def create_assignment(
        self,
        title: str,
        type: str,
        description: Optional[str],
        course_id: str,
        current_user_id: UUID,
        due_at: Optional[str],
        score: Optional[int] = 0,
    ):
        course = self.course_service.retrieve_course(course_id, current_user_id)
        new_assignment = Assignment(
            title=title,
            type=type,
            description=description,
            course=course,
            due_at=due_at,
            score=score,
        )
        return self.repository.create_assignment(new_assignment)

    def list_assignments(self, user_id: UUID, course_id: Optional[str] = None):
        if course_id:
            self.course_service.retrieve_course(course_id, user_id)
        return self.repository.list_assignments(user_id, course_id)

    def retrieve_assignment(self, assignment_id: str, current_user_id: UUID):
        assignment = self.repository.retrieve_assignment(assignment_id)
        if not assignment or assignment.course.user_id != current_user_id:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return assignment

    def update_assignment(
        self,
        assignment_id: str,
        current_user_id: UUID,
        course_id: Optional[str] = None,
        title: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        due_at: Optional[str] = None,
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

    def delete_assignment(self, assignment_id: str, current_user_id: UUID):
        assignment = self.retrieve_assignment(assignment_id, current_user_id)
        return self.repository.delete_assignment(assignment.id)
