"""Re-export the ORM models and helpers from ``src.models``.

Keeping a thin compatibility layer lets existing imports like
``from models import Task`` continue working while the actual code stays inside
``src/`` for a cleaner project layout.
"""

from src.models import (  # noqa: F401
    Base,
    DEFAULT_SQLITE_URL,
    SQLALCHEMY_DATABASE_URL,
    SessionLocal,
    Task,
    engine,
    get_db,
    init_db,
)

__all__ = [
    "Base",
    "DEFAULT_SQLITE_URL",
    "SQLALCHEMY_DATABASE_URL",
    "SessionLocal",
    "Task",
    "engine",
    "get_db",
    "init_db",
]
