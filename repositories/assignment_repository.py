from typing import List, Optional
from uuid import UUID

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.assignment import Assignment
from models.course import Course
from models.term import Term


class AssignmentRepository(BaseRepository):
    def create_assignment(self, assignment: Assignment) -> Assignment:
        try:
            self.db.add(assignment)
            self.db.commit()
            self.db.refresh(assignment)
            return assignment
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def retrieve_assignment(self, assignment_id: UUID) -> Assignment:
        try:
            return (
                self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def update_assignment(self, assignment: Assignment) -> Assignment:
        try:
            self.db.merge(assignment)
            self.db.commit()
            self.db.refresh(assignment)
            return assignment
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            )

    def delete_assignment(self, assignment_id: UUID) -> None:
        try:
            assignment = (
                self.db.query(Assignment).filter(Assignment.id == assignment_id).first()
            )

            self.db.delete(assignment)
            self.db.commit()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            )

    def list_assignments(
        self, user_id: Optional[UUID] = None, course_id: Optional[UUID] = None
    ) -> List[Assignment]:
        try:
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
                    .join(Term)
                    .filter(Term.user_id == user_id)
                    .all()
                )

            return self.db.query(Assignment).all()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            )
