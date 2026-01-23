"""Unit tests for User model"""
import pytest
from datetime import datetime


def test_user_model_creation(db_session, sample_user_data):
    """Test creating a User model instance"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.email == sample_user_data["email"]
    assert user.username == sample_user_data["username"]
    assert user.hashed_password == sample_user_data["hashed_password"]


def test_user_model_required_fields(db_session):
    """Test that required fields are enforced"""
    from user import User
    from sqlalchemy.exc import IntegrityError

    # Try to create user without email
    user = User(
        username="testuser",
        hashed_password="test_hash"
    )
    db_session.add(user)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_user_email_uniqueness(db_session, sample_user_data):
    """Test that email must be unique"""
    from user import User
    from sqlalchemy.exc import IntegrityError

    # Create first user
    user1 = User(**sample_user_data)
    db_session.add(user1)
    db_session.commit()

    # Try to create another user with same email
    sample_user_data["username"] = "anotheruser"
    user2 = User(**sample_user_data)
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_user_username_uniqueness(db_session, sample_user_data):
    """Test that username must be unique"""
    from user import User
    from sqlalchemy.exc import IntegrityError

    # Create first user
    user1 = User(**sample_user_data)
    db_session.add(user1)
    db_session.commit()

    # Try to create another user with same username
    sample_user_data["email"] = "another@example.com"
    user2 = User(**sample_user_data)
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_user_default_values(db_session):
    """Test default values for User model"""
    from user import User

    user = User(
        email="default@test.com",
        username="defaultuser",
        hashed_password="test_hash"
    )
    db_session.add(user)
    db_session.commit()

    assert user.is_active is True
    assert user.is_superuser is False
    assert user.full_name is None


def test_user_timestamps(db_session, sample_user_data):
    """Test that timestamps are set automatically"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    assert user.created_at is not None
    assert user.updated_at is not None
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_repr(db_session, sample_user_data):
    """Test User model __repr__ method"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    repr_str = repr(user)
    assert "User" in repr_str
    assert str(user.id) in repr_str
    assert user.username in repr_str
    assert user.email in repr_str


def test_user_is_active_flag(db_session, sample_user_data):
    """Test is_active flag"""
    from user import User

    sample_user_data["is_active"] = False
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    assert user.is_active is False


def test_user_is_superuser_flag(db_session, sample_user_data):
    """Test is_superuser flag"""
    from user import User

    sample_user_data["is_superuser"] = True
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    assert user.is_superuser is True


def test_user_full_name_optional(db_session):
    """Test that full_name is optional"""
    from user import User

    user = User(
        email="noname@test.com",
        username="nonameuser",
        hashed_password="test_hash"
    )
    db_session.add(user)
    db_session.commit()

    assert user.full_name is None

    # Now add a full name
    user.full_name = "Test User"
    db_session.commit()

    assert user.full_name == "Test User"


def test_user_query_by_email(db_session, sample_user_data):
    """Test querying user by email"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    found_user = db_session.query(User).filter_by(email=sample_user_data["email"]).first()
    assert found_user is not None
    assert found_user.email == sample_user_data["email"]


def test_user_query_by_username(db_session, sample_user_data):
    """Test querying user by username"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    found_user = db_session.query(User).filter_by(username=sample_user_data["username"]).first()
    assert found_user is not None
    assert found_user.username == sample_user_data["username"]


def test_user_update(db_session, sample_user_data):
    """Test updating user data"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    # Update user data
    user.full_name = "Updated Name"
    user.is_active = False
    db_session.commit()

    # Verify updates
    updated_user = db_session.query(User).filter_by(id=user.id).first()
    assert updated_user.full_name == "Updated Name"
    assert updated_user.is_active is False


def test_user_delete(db_session, sample_user_data):
    """Test deleting a user"""
    from user import User

    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()

    user_id = user.id

    # Delete user
    db_session.delete(user)
    db_session.commit()

    # Verify deletion
    deleted_user = db_session.query(User).filter_by(id=user_id).first()
    assert deleted_user is None
