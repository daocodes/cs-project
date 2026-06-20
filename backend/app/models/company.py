from app.db.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )  # primarykey means a unique value in each row
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)

    job_postings = relationship("JobPosting", back_populates="company")
