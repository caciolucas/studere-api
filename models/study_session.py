import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base
from models.study_plan import study_session_topics

if TYPE_CHECKING:
    from models.study_plan import StudyPlan, StudyPlanTopic


class SessionState(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    notes = mapped_column(Text, nullable=True)

    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("study_plans.id"), nullable=False
    )
    plan: Mapped["StudyPlan"] = relationship("StudyPlan", back_populates="sessions")

    topics: Mapped[List["StudyPlanTopic"]] = relationship(
        "StudyPlanTopic", secondary=study_session_topics, back_populates="sessions"
    )

    status: Mapped[SessionState] = mapped_column(
        String, default=SessionState.ACTIVE.value
    )

    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    last_pause_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    total_pause_time: Mapped[float] = mapped_column(Float, default=0.0)
    study_time: Mapped[float] = mapped_column(Float, default=0.0)
