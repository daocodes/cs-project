import enum

from app.db.base import Base
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ApplicationStatus(str, enum.Enum):
    SAVED = "SAVED"
    APPLIED = "APPLIED"
    OA = "OA"
    PHONE_SCREEN = "PHONE_SCREEN"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    ONSITE = "ONSITE"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    GHOSTED = "GHOSTED"
    WITHDRAWN = "WITHDRAWN"


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )  # primarykey means a unique value in each row
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )  # foreignkey means that it needs to match to an existing user id
    job_posting_id: Mapped[int] = mapped_column(
        ForeignKey("job_postings.id"), nullable=False
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), nullable=False
    )
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="applications")
    job_posting = relationship("JobPosting", back_populates="applications")
    status_events = relationship(
        "StatusEvent", back_populates="application", cascade="all, delete-orphan"
    )
