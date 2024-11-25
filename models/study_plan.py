from typing import TYPE_CHECKING, List
import uuid

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base

study_session_topics = Table(
    "study_session_topics",
    Base.metadata,
    Column("session_id", UUID(as_uuid=True), ForeignKey("study_sessions.id")),
    Column("topic_id", UUID(as_uuid=True), ForeignKey("study_plan_topics.id")),
)

if TYPE_CHECKING:
    from models.course import Course
    from models.study_session import StudySession


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE")
    )

    course: Mapped["Course"] = relationship("Course", back_populates="plans")

    topics: Mapped[List["StudyPlanTopic"]] = relationship(
        "StudyPlanTopic", back_populates="plan", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["StudySession"]] = relationship(
        "StudySession", back_populates="plan", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class StudyPlanTopic(Base):
    __tablename__ = "study_plan_topics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("study_plans.id")
    )
    plan: Mapped["StudyPlan"] = relationship("StudyPlan", back_populates="topics")

    sessions: Mapped[List["StudySession"]] = relationship(
        "StudySession", secondary=study_session_topics, back_populates="topics"
    )

    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
