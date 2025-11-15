"""Pydantic schemas that define the public contract of the API.

The schemas are responsible for validating data coming in via requests and for
serialising ORM objects back to JSON responses. Keeping them decoupled from the
ORM models lets us evolve each layer independently.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class TaskBase(BaseModel):
    """Fields common to all task operations."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(
        None, min_length=1, max_length=10_000, description="Detailed task notes"
    )


class TaskCreate(TaskBase):
    """Payload required to create a new task."""

    is_completed: bool = Field(False, description="Allow creating a task as done")


class TaskUpdate(BaseModel):
    """Payload for updating existing tasks (PATCH semantics)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=10_000)
    is_completed: Optional[bool] = None

    class Config:
        # Reject completely empty bodies so the handler can respond 400 early.
        min_anystr_length = 1
        anystr_strip_whitespace = True

    @root_validator(pre=True)
    def check_not_empty(cls, values: dict) -> dict:
        """Ensure the request includes at least one field to change."""

        if not values or all(value is None for value in values.values()):
            raise ValueError("At least one field must be provided")
        return values


class Task(TaskBase):
    """Response model returned by the API."""

    id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
