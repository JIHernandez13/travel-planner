import os

os.environ.setdefault(
    "DATABASE_URL", "sqlite:///test.db"
)
os.environ.setdefault(
    "SECRET_KEY", "test-secret-key-not-for-production"
)

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from database import Base, engine  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app."""
    return TestClient(app)
