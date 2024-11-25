import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, String, ForeignKey, Date, func
from sqlalchemy.orm import mapped_column, Mapped
from db.session import Base


if TYPE_CHECKING:
    from models.course import Course
    from models.user import User


class Term(Base):
    __tablename__ = "terms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship("User", back_populates="terms")

    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    courses: Mapped[List["Course"]] = relationship(
        "Course", back_populates="term", cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
