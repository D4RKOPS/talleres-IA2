"""Database models and session setup for the QuickTask API.

This module defines the SQLAlchemy ORM model for tasks and exposes the
SQLAlchemy engine, session factory and helper utilities used across the
application. Keeping everything in one place keeps the data layer easy
to reason about for a small project like this.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Generator
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# SQLAlchemy configuration
# ---------------------------------------------------------------------------

# SQLite database stored locally in the repo directory. `check_same_thread`
# must be disabled when the connection is shared across threads (FastAPI
# creates a new session per request but the engine is module-level).
DEFAULT_SQLITE_URL = "sqlite:///./tasks.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

connect_args: dict[str, Any] = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# Session factory bound to the engine. `autocommit` and `autoflush` are disabled
# so transactions are controlled explicitly for predictability.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models in the project.
Base = declarative_base()


# ---------------------------------------------------------------------------
# ORM model definitions
# ---------------------------------------------------------------------------


class Task(Base):
    """Persistent representation of a user's task.

    Attributes:
        id: Primary key stored as a UUID string for easier client consumption.
        title: Short description of the task (required).
        description: Optional longer text with additional details.
        is_completed: Boolean flag indicating if the task is done.
        created_at: Timestamp of when the task was first inserted.
        updated_at: Timestamp automatically bumped on updates.
    """

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def init_db() -> None:
    """Create database tables if they do not exist yet."""

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """Yield a SQLAlchemy session to be used inside request handlers.

    The session is automatically closed once the FastAPI dependency scope ends.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
