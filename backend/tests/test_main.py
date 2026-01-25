"""Unit tests for main FastAPI application"""


def test_app_creation(client):
    """Test that the FastAPI app is created successfully"""
    from app.main import app

    assert app is not None
    assert app.title == "Travel Planner API"


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["message"] == "Welcome to Travel Planner API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"


def test_health_check_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_cors_middleware(test_env):
    """Test that CORS middleware is configured"""
    from app.main import app

    # Check that CORS middleware is added
    middlewares = [m for m in app.user_middleware]
    assert len(middlewares) > 0


def test_app_metadata(test_env):
    """Test FastAPI app metadata"""
    from app.main import app

    assert app.title == "Travel Planner API"
    assert app.version == "1.0.0"
    assert app.description == "Travel Planner API - Plan and organize your trips"


def test_openapi_schema(client):
    """Test that OpenAPI schema is available"""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Travel Planner API"
    assert schema["info"]["version"] == "1.0.0"


def test_docs_endpoint(client):
    """Test that API documentation is available"""
    response = client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_root_endpoint_returns_json(client):
    """Test that root endpoint returns JSON"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_returns_json(client):
    """Test that health endpoint returns JSON"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_nonexistent_endpoint(client):
    """Test that nonexistent endpoints return 404"""
    response = client.get("/nonexistent")

    assert response.status_code == 404


def test_cors_headers_configuration(test_env):
    """Test CORS headers configuration"""
    from config import settings

    assert "http://localhost:5173" in settings.ALLOWED_ORIGINS
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS
