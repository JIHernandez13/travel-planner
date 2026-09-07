"""Pytest configuration and shared fixtures for backend tests"""
import os
import sys
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set env vars at module level so config.py can be imported safely
# during pytest collection and coverage instrumentation
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only-do-not-use-in-production")
os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("DEBUG", "False")


@pytest.fixture(scope="function")
def test_env():
    """Set up test environment variables"""
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only-do-not-use-in-production"
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DEBUG"] = "False"


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a test database session"""
    from database import Base

    import user  # noqa: F401

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app"""
    from main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": ("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/"
                            "LewY5GyYZ7WMuB15u"),
        "full_name": "Test User",
        "is_active": True,
        "is_superuser": False,
    }
