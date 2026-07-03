import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.deps import get_current_user
from app.auth.types import CurrentUser
from app.db.base import Base
from app.db.deps import get_db
from app.models.company import Company
from app.models.job_posting import JobPosting
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
def auth_context():
    return {"id": 1, "email": "student@example.com", "auth_id": "mock-auth-1"}


@pytest.fixture()
def client(db_session, auth_context):
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return CurrentUser(
            id=auth_context["id"],
            email=auth_context["email"],
            auth_id=auth_context["auth_id"],
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def job_posting(db_session):
    company = Company(name="Acme Corp")
    db_session.add(company)
    db_session.commit()

    posting = JobPosting(company_id=company.id, title="SWE Intern", is_internship=True)
    db_session.add(posting)
    db_session.commit()

    return {"job_posting_id": posting.id}
