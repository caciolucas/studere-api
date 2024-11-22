import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey, Table, Text, Float, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base

study_session_topics = Table(
    "study_session_topics",
    Base.metadata,
    Column("session_id", UUID(as_uuid=True), ForeignKey("study_sessions.id")),
    Column("topic_id", UUID(as_uuid=True), ForeignKey("study_plan_topics.id")),
)


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    notes = Column(Text, nullable=True)

    plan_id = Column(UUID(as_uuid=True), ForeignKey("study_plans.id"), nullable=False)
    plan = relationship("StudyPlan", back_populates="sessions")

    topics = relationship(
        "StudyPlanTopic", secondary=study_session_topics, back_populates="sessions"
    )

    # State fields
    is_active = Column(Boolean, default=True)
    is_paused = Column(Boolean, default=False)

    # Timing fields
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)

    last_pause_time = Column(DateTime, nullable=True)
    total_pause_time = Column(Float, default=0.0)
