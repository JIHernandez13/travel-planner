from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import os

# Build engine kwargs based on database type
engine_kwargs = {
    "echo": settings.DEBUG,
}

# SQLite does not support pool_size or pool_pre_ping
if not settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = int(
        os.getenv("DB_POOL_SIZE", "5")
    )
    engine_kwargs["max_overflow"] = int(
        os.getenv("DB_MAX_OVERFLOW", "10")
    )
else:
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }

# Create database engine with configurable pool settings
engine = create_engine(
    settings.DATABASE_URL,
    **engine_kwargs
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
