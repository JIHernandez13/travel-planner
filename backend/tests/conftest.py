import os

os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
