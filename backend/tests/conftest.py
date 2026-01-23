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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables"""
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only-do-not-use-in-production"
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DEBUG"] = "False"


@pytest.fixture(scope="function")
def db_session(test_env) -> Generator[Session, None, None]:
    """Create a test database session"""
    # Import here to ensure environment is set up first
    from database import Base
    # Import models to register them with Base
    import user  # noqa: F401

    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(test_env) -> Generator[TestClient, None, None]:
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
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYZ7WMuB15u",  # "password"
        "full_name": "Test User",
        "is_active": True,
        "is_superuser": False,
    }
