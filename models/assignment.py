import uuid
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class AssignmentType(Enum):
    PROJECT = "project"
    EXAM = "exam"


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    course = relationship("Course", back_populates="assignments")

    score = Column(Integer, nullable=True, default=0)
    due_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
