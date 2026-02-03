"""Tests for authentication endpoints."""


def _register_user(client, **overrides):
    """Helper to register a test user."""
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123",
        "full_name": "Test User",
    }
    data.update(overrides)
    return client.post("/api/v1/auth/register", json=data)


def _login_user(client, username="testuser",
                password="securepassword123"):
    """Helper to login a test user."""
    return client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )


class TestRegister:
    """Tests for POST /api/v1/auth/register."""

    def test_register_success(self, client):
        """Register with valid data returns 201."""
        response = _register_user(client)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["full_name"] == "Test User"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        # Password should not be in response
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client):
        """Register with duplicate email returns 400."""
        _register_user(client)
        response = _register_user(
            client, username="otheruser"
        )
        assert response.status_code == 400
        assert "Email already registered" in (
            response.json()["detail"]
        )

    def test_register_duplicate_username(self, client):
        """Register with duplicate username returns 400."""
        _register_user(client)
        response = _register_user(
            client, email="other@example.com"
        )
        assert response.status_code == 400
        assert "Username already taken" in (
            response.json()["detail"]
        )


class TestLogin:
    """Tests for POST /api/v1/auth/login."""

    def test_login_success(self, client):
        """Login with valid credentials returns token."""
        _register_user(client)
        response = _login_user(client)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Login with wrong password returns 401."""
        _register_user(client)
        response = _login_user(
            client, password="wrongpassword"
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in (
            response.json()["detail"]
        )

    def test_login_nonexistent_user(self, client):
        """Login with nonexistent user returns 401."""
        response = _login_user(
            client, username="nouser"
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in (
            response.json()["detail"]
        )

    def test_login_with_email(self, client):
        """Login with email instead of username works."""
        _register_user(client)
        response = _login_user(
            client, username="test@example.com"
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestGetMe:
    """Tests for GET /api/v1/auth/me."""

    def test_get_me_authenticated(self, client):
        """Get current user with valid token returns 200."""
        _register_user(client)
        login_response = _login_user(client)
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_me_no_token(self, client):
        """Get current user without token returns 401."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
