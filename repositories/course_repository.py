from core.repository import BaseRepository
from models.course import Course


class CourseRepository(BaseRepository):
    def create_course(self, course: Course) -> Course:
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def retrieve_course(self, course_id: str) -> Course:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def update_course(self, course: Course) -> Course:
        self.db.merge(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course_id: str) -> None:
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if course:
            self.db.delete(course)
            self.db.commit()

    def list_courses(self, user_id) -> list[Course]:
        if user_id:
            return self.db.query(Course).filter(Course.user_id == user_id).all()
        return self.db.query(Course).all()
