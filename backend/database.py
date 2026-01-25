from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import os

# Create database engine with configurable pool settings
# SQLite doesn't support pool_size and max_overflow
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL, echo=settings.DEBUG, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
