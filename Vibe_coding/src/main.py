"""Entry point for the QuickTask FastAPI application."""

from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
from models import Task as TaskModel
from models import get_db, init_db
from schemas import Task, TaskCreate, TaskUpdate

app = FastAPI(title="QuickTask API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    """Initialise the SQLite database once the application boots."""

    init_db()


@app.get("/tasks", response_model=List[Task], summary="List all tasks")
def read_tasks(db: Session = Depends(get_db)) -> List[TaskModel]:
    """Return all stored tasks ordered by creation time."""

    return list(crud.list_tasks(db))


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)) -> TaskModel:
    """Persist a new task and return the stored representation."""

    return crud.create_task(db, task_in)


@app.put("/tasks/{task_id}", response_model=Task, summary="Replace a task")
def replace_task(
    task_id: str, task_in: TaskCreate, db: Session = Depends(get_db)
) -> TaskModel:
    """Replace all data of an existing task (PUT semantics)."""

    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Reuse the partial update helper by building a TaskUpdate payload that
    # contains all fields. This keeps logic centralised in the crud module.
    update_payload = TaskUpdate(**task_in.dict())
    return crud.update_task(db, task, update_payload)


@app.patch("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task(
    task_id: str, task_in: TaskUpdate, db: Session = Depends(get_db)
) -> TaskModel:
    """Apply a partial update to an existing task (PATCH semantics)."""

    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return crud.update_task(db, task, task_in)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    """Remove a task permanently."""

    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    crud.delete_task(db, task)


@app.get("/tasks/{task_id}", response_model=Task, summary="Retrieve a task")
def read_task(task_id: str, db: Session = Depends(get_db)) -> TaskModel:
    """Return a single task by identifier."""

    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
