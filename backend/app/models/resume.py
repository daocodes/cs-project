# backend/app/models/resume.py
from app.db.base import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    s3_key: Mapped[str | None] = mapped_column(String(512), nullable=True)
    parsed_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="resumes")
