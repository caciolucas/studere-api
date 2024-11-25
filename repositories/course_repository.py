from core.repository import BaseRepository
from models.course import Course
from typing import Optional
from uuid import UUID
from models.term import Term


class CourseRepository(BaseRepository):
    def create_course(self, course: Course) -> Course:
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def retrieve_course(self, course_id: UUID) -> Course:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def update_course(self, course: Course) -> Course:
        self.db.merge(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course_id: UUID) -> None:
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if course:
            self.db.delete(course)
            self.db.commit()

    def list_courses(
        self, user_id: UUID, term_id: Optional[UUID] = None
    ) -> list[Course]:
        if term_id:
            return self.db.query(Course).filter(Course.term_id == term_id).all()

        return (
            self.db.query(Course)
            .join(Term, Term.id == Course.term_id)
            .filter(Term.user_id == user_id)
            .all()
        )
