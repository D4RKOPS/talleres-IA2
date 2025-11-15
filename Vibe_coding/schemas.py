"""Compatibility wrapper for the Pydantic schemas located in ``src.schemas``."""

from src.schemas import (  # noqa: F401
    Task,
    TaskBase,
    TaskCreate,
    TaskUpdate,
)

__all__ = ["Task", "TaskBase", "TaskCreate", "TaskUpdate"]
