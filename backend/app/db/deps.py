from app.db.base import Base  # noqa: F401 — registers all models before any router imports one directly
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
