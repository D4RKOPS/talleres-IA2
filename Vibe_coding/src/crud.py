"""Encapsulated database operations for the Task entity."""

from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from models import Task
from schemas import TaskCreate, TaskUpdate


def list_tasks(db: Session) -> Iterable[Task]:
    """Return all tasks sorted by creation date (newest first)."""

    return db.query(Task).order_by(Task.created_at.desc()).all()


def get_task(db: Session, task_id: str) -> Optional[Task]:
    """Retrieve a single task by its identifier."""

    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task_in: TaskCreate) -> Task:
    """Persist a new task in the database."""

    task = Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    """Update an existing task with partial data provided by the client."""

    for field, value in task_in.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """Remove the given task from the database."""

    db.delete(task)
    db.commit()
