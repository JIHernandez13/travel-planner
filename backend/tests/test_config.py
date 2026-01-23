"""Unit tests for configuration module"""
import os


def test_settings_default_values(test_env):
    """Test that settings have correct default values"""
    from config import Settings

    settings = Settings()

    assert settings.PROJECT_NAME == "Travel Planner API"
    assert settings.VERSION == "1.0.0"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60
    assert settings.REFRESH_TOKEN_EXPIRE_MINUTES == 60 * 24 * 7
    assert settings.ENVIRONMENT == "testing"
    assert settings.DEBUG is False


def test_settings_custom_values(test_env):
    """Test that settings can be customized via environment"""
    os.environ["PROJECT_NAME"] = "Custom API"
    os.environ["VERSION"] = "2.0.0"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "120"

    from config import Settings
    settings = Settings()

    assert settings.PROJECT_NAME == "Custom API"
    assert settings.VERSION == "2.0.0"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 120

    # Clean up
    del os.environ["PROJECT_NAME"]
    del os.environ["VERSION"]
    del os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]


def test_settings_allowed_origins(test_env):
    """Test CORS allowed origins configuration"""
    from config import Settings

    settings = Settings()

    assert isinstance(settings.ALLOWED_ORIGINS, list)
    assert "http://localhost:5173" in settings.ALLOWED_ORIGINS
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS


def test_settings_database_url_required(test_env):
    """Test that DATABASE_URL is properly set"""
    from config import Settings

    settings = Settings()
    assert settings.DATABASE_URL == "sqlite:///:memory:"


def test_settings_secret_key_required(test_env):
    """Test that SECRET_KEY is properly set"""
    from config import Settings

    settings = Settings()
    assert settings.SECRET_KEY == "test-secret-key-for-testing-only-do-not-use-in-production"


def test_settings_case_sensitive(test_env):
    """Test that settings are case sensitive"""
    from config import Settings

    settings = Settings()

    # The Config class has case_sensitive = True
    assert hasattr(settings.Config, 'case_sensitive')
    assert settings.Config.case_sensitive is True


def test_settings_refresh_token_expiry(test_env):
    """Test refresh token expiry calculation"""
    from config import Settings

    settings = Settings()

    # 7 days = 7 * 24 * 60 = 10080 minutes
    expected_minutes = 7 * 24 * 60
    assert settings.REFRESH_TOKEN_EXPIRE_MINUTES == expected_minutes
