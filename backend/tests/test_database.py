"""Unit tests for database module"""
from sqlalchemy.orm import Session


def test_database_session_creation(db_session):
    """Test that database session is created successfully"""
    assert db_session is not None
    assert isinstance(db_session, Session)


def test_get_db_function(test_env):
    """Test the get_db dependency function"""
    from database import get_db

    # Get the generator
    db_gen = get_db()

    # Get the session
    db = next(db_gen)
    assert db is not None
    assert isinstance(db, Session)

    # Close the session
    try:
        next(db_gen)
    except StopIteration:
        pass  # Expected behavior


def test_base_declarative(test_env):
    """Test that Base is a valid declarative base"""
    from database import Base
    from sqlalchemy.ext.declarative import DeclarativeMeta

    assert isinstance(Base, DeclarativeMeta)


def test_engine_configuration(test_env):
    """Test database engine configuration"""
    from database import engine

    assert engine is not None
    # Test that we can connect
    connection = engine.connect()
    assert connection is not None
    connection.close()


def test_session_local_factory(test_env):
    """Test SessionLocal factory configuration"""
    from database import SessionLocal

    assert SessionLocal is not None

    # Create a session
    session = SessionLocal()
    assert isinstance(session, Session)
    session.close()


def test_session_transaction_rollback(db_session):
    """Test that sessions can be rolled back"""
    from user import User

    # Create and commit a user first
    user = User(
        email="initial@test.com",
        username="initialuser",
        hashed_password="test_hash"
    )
    db_session.add(user)
    db_session.commit()

    # Now test rollback with a nested transaction
    db_session.begin_nested()
    user2 = User(
        email="rollback@test.com",
        username="rollbackuser",
        hashed_password="test_hash"
    )
    db_session.add(user2)
    db_session.rollback()

    # Verify second user was not persisted
    result = db_session.query(User).filter_by(email="rollback@test.com").first()
    assert result is None

    # Verify first user is still there
    result = db_session.query(User).filter_by(email="initial@test.com").first()
    assert result is not None


def test_session_transaction_commit(db_session):
    """Test that sessions can commit transactions"""
    from user import User

    # Add a test user
    user = User(
        email="commit@test.com",
        username="commituser",
        hashed_password="test_hash"
    )
    db_session.add(user)
    db_session.commit()

    # Verify user was persisted
    result = db_session.query(User).filter_by(email="commit@test.com").first()
    assert result is not None
    assert result.email == "commit@test.com"
