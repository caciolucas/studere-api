from typing import TYPE_CHECKING, List
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base

if TYPE_CHECKING:
    from models.assignment import Assignment
    from models.study_plan import StudyPlan
    from models.term import Term


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    term_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("terms.id", ondelete="CASCADE")
    )
    term: Mapped["Term"] = relationship("Term", back_populates="courses")

    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", back_populates="course", cascade="all, delete-orphan"
    )
    plans: Mapped[List["StudyPlan"]] = relationship(
        "StudyPlan", back_populates="course", cascade="all, delete-orphan"
    )
