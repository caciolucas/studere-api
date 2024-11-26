from typing import Optional
from uuid import UUID

from core.exceptions import RepositoryError
from core.repository import BaseRepository
from models.course import Course
from models.term import Term


class CourseRepository(BaseRepository):
    def create_course(self, course: Course) -> Course:
        try:
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def retrieve_course(self, course_id: UUID) -> Course:
        try:
            return self.db.query(Course).filter(Course.id == course_id).first()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def update_course(self, course: Course) -> Course:
        try:
            self.db.merge(course)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def delete_course(self, course_id: UUID) -> None:
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            self.db.delete(course)
            self.db.commit()
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e

    def list_courses(
        self, user_id: UUID, term_id: Optional[UUID] = None
    ) -> list[Course]:
        try:
            if term_id:
                return self.db.query(Course).filter(Course.term_id == term_id).all()

            return (
                self.db.query(Course)
                .join(Term, Term.id == Course.term_id)
                .filter(Term.user_id == user_id)
                .all()
            )
        except Exception as e:
            raise RepositoryError(
                f"Operation failed due to internal database error: {e}"
            ) from e
