"""Unit and integration tests for QuickTask CRUD endpoints."""

from __future__ import annotations

from typing import Tuple

from models import Task


def _persist_task(session_factory, **overrides) -> Task:
    """Helper to persist a task directly in the database for setup."""

    defaults = {"title": "Sample task", "description": "Seeded description"}
    defaults.update(overrides)

    with session_factory() as session:
        task = Task(**defaults)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


def test_create_task_returns_201_and_payload(test_client: Tuple) -> None:
    client, _ = test_client

    payload = {"title": "Comprar café", "description": "Granos tostados", "is_completed": False}

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_completed"] is False


def test_list_tasks_returns_existing_records(test_client: Tuple) -> None:
    client, session_factory = test_client

    _persist_task(session_factory, title="Tarea A")
    _persist_task(session_factory, title="Tarea B", is_completed=True)

    response = client.get("/tasks")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    titles = [task["title"] for task in tasks]
    assert "Tarea A" in titles and "Tarea B" in titles


def test_patch_task_updates_fields(test_client: Tuple) -> None:
    client, session_factory = test_client
    task = _persist_task(session_factory)

    response = client.patch(
        f"/tasks/{task.id}",
        json={"title": "Actualizada", "is_completed": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Actualizada"
    assert body["is_completed"] is True

    # Confirm persisted changes
    with session_factory() as session:
        refreshed = session.get(Task, task.id)
        assert refreshed is not None
        assert refreshed.title == "Actualizada"
        assert refreshed.is_completed is True


def test_delete_task_removes_record(test_client: Tuple) -> None:
    client, session_factory = test_client
    task = _persist_task(session_factory)

    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204

    with session_factory() as session:
        assert session.get(Task, task.id) is None