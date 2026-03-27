import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from schemas.tasks import TaskCreateSchema
from services.tasks import TaskService
from repositories.tasks import TaskRepository
from main import app
from core.database import Base, engine, get_db
from models.users import User
from core.security import create_access_token

def test_task_service_create_task():
    # Arrange
    mock_repo = MagicMock(spec=TaskRepository)
    task_service = TaskService(repository=mock_repo)
    
    task_in = TaskCreateSchema(title="Test Task", description="Test desc", is_completed=False)
    user_id = 1
    
    class MockTask:
        id = 1
        title = "Test Task"
        description = "Test desc"
        is_completed = False
        owner_id = user_id

    mock_repo.create.return_value = MockTask()
    
    # Act
    result = task_service.create_task(task=task_in, user_id=user_id)
    
    # Assert
    mock_repo.create.assert_called_once_with(task=task_in, user_id=user_id)
    assert result.id == 1
    assert result.title == "Test Task"
    assert result.owner_id == user_id

def test_create_task_integration(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task_data = {
        "title": "Integration Task",
        "description": "testing",
        "is_completed": False
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Integration Task"
    assert data["description"] == "testing"
    assert data["is_completed"] is False
    assert "id" in data

def test_create_task_validation_error(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Title less than 3 symbols
    task_data = {"title": "ab"}
    response = client.post("/tasks/", json=task_data, headers=headers)
    
    assert response.status_code == 422

def test_get_tasks(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/tasks/", json={"title": "Task 1"}, headers=headers)
    client.post("/tasks/", json={"title": "Task 2"}, headers=headers)
    
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_task_by_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_res = client.post("/tasks/", json={"title": "Specific Task"}, headers=headers)
    task_id = create_res.json()["id"]
    
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"

def test_get_task_not_found_or_forbidden(client, auth_token, second_auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_res = client.post("/tasks/", json={"title": "My Private Task"}, headers=headers)
    task_id = create_res.json()["id"]
    
    # Пытаемся получить несуществующую задачу
    res_not_found = client.get("/tasks/999", headers=headers)
    assert res_not_found.status_code == 404
    assert res_not_found.json()["error"]["code"] == "TASK_NOT_FOUND"

    # Пытаемся получить задачу другого пользователя
    second_headers = {"Authorization": f"Bearer {second_auth_token}"}
    res_forbidden = client.get(f"/tasks/{task_id}", headers=second_headers)
    assert res_forbidden.status_code == 404

def test_update_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_res = client.post("/tasks/", json={"title": "Old Title"}, headers=headers)
    task_id = create_res.json()["id"]
    
    response = client.patch(f"/tasks/{task_id}", json={"title": "New Title", "is_completed": True}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["is_completed"] is True

def test_delete_task(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_res = client.post("/tasks/", json={"title": "Task for delete"}, headers=headers)
    task_id = create_res.json()["id"]
    
    del_res = client.delete(f"/tasks/{task_id}", headers=headers)
    assert del_res.status_code == 204
    
    check_res = client.get(f"/tasks/{task_id}", headers=headers)
    assert check_res.status_code == 404
