import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base

study_session_topics = Table(
    "study_session_topics",
    Base.metadata,
    Column("session_id", UUID(as_uuid=True), ForeignKey("study_sessions.id")),
    Column("topic_id", UUID(as_uuid=True), ForeignKey("study_plan_topics.id")),
)


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    course = relationship("Course", back_populates="plans")

    topics = relationship(
        "StudyPlanTopic", back_populates="plan", cascade="all, delete-orphan"
    )
    sessions = relationship(
        "StudySession", back_populates="plan", cascade="all, delete-orphan"
    )
    created_at = Column(DateTime, server_default=func.now())


class StudyPlanTopic(Base):
    __tablename__ = "study_plan_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)

    plan_id = Column(UUID(as_uuid=True), ForeignKey("study_plans.id"))
    plan = relationship("StudyPlan", back_populates="topics")

    sessions = relationship(
        "StudySession", secondary=study_session_topics, back_populates="topics"
    )

    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
