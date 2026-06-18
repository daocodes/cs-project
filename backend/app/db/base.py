from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so Alembic can discover metadata
from app.models.application import Application  # noqa: E402,F401
from app.models.company import Company  # noqa: E402,F401
from app.models.job_posting import JobPosting  # noqa: E402,F401
from app.models.resume import Resume  # noqa: E402,F401
from app.models.status_event import StatusEvent  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401
