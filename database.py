from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from config import settings


# SQLite Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)


# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base Model
class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    """
    Returns a database session.
    Automatically closes the session after use.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Create Tables
def create_database():
    """
    Creates all database tables.
    """
    Base.metadata.create_all(bind=engine)
