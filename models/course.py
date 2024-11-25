import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)

    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE"))
    term = relationship("Term", back_populates="courses")

    assignments = relationship(
        "Assignment", back_populates="course", cascade="all, delete-orphan"
    )
    plans = relationship(
        "StudyPlan", back_populates="course", cascade="all, delete-orphan"
    )
