from typing import Optional
from uuid import UUID

from core.repository import BaseRepository
from models.assignment import Assignment
from models.course import Course


class AssignmentRepository(BaseRepository):
    def create_assignment(self, assignment: Assignment) -> Assignment:
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def retrieve_assignment(self, assignment_id: UUID) -> Assignment:
        return self.db.query(Assignment).filter(Assignment.id == assignment_id).first()

    def update_assignment(self, assignment: Assignment) -> Assignment:
        self.db.merge(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete_assignment(self, assignment_id: UUID) -> None:
        assignment = (
            self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
        )
        if assignment:
            self.db.delete(assignment)
            self.db.commit()

    def list_assignments(
        self, user_id: Optional[UUID] = None, course_id: Optional[UUID] = None
    ) -> list[Assignment]:
        if course_id:
            return (
                self.db.query(Assignment)
                .filter(Assignment.course_id == course_id)
                .all()
            )

        if user_id:
            return (
                self.db.query(Assignment)
                .join(Course)
                .filter(Course.user_id == user_id)
                .all()
            )

        return self.db.query(Assignment).all()
