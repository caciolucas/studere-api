import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.session import Base


class Term(Base):
    __tablename__ = "terms"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="terms")

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    courses = relationship(
        "Course", back_populates="term", cascade="all, delete-orphan"
    )
    created_at = Column(DateTime, server_default=func.now())
