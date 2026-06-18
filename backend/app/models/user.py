# backend/app/models/user.py
from app.db.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    applications = relationship("Application", back_populates="user")
    resumes = relationship("Resume", back_populates="user")
