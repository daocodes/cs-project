import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.deps import get_db
from app.models.company import Company
from app.models.job_posting import JobPosting
from app.models.user import User
from main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def job_posting(db_session):
    user = User(email="student@example.com")
    company = Company(name="Acme Corp")
    db_session.add_all([user, company])
    db_session.commit()

    posting = JobPosting(company_id=company.id, title="SWE Intern", is_internship=True)
    db_session.add(posting)
    db_session.commit()

    return {"user_id": user.id, "job_posting_id": posting.id}
