"""Compatibility wrapper for the CRUD helpers stored under ``src.crud``."""

from src.crud import (  # noqa: F401
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)

__all__ = [
    "create_task",
    "delete_task",
    "get_task",
    "list_tasks",
    "update_task",
]
