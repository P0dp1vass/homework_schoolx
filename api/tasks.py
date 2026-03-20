from fastapi import APIRouter, status, Depends
from typing import List

from dependency import get_current_user
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from services.tasks import TaskService
from models.users import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreateSchema,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return service.create_task(task=task, user_id=user.id)

@router.get("/", response_model=List[TaskResponseSchema])
def get_all_tasks(
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return service.get_all_tasks(user_id=user.id)

@router.get("/{task_id}", response_model=TaskResponseSchema)
def get_task(
    task_id: int,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return service.get_task(task_id=task_id, user_id=user.id)

@router.patch("/{task_id}", response_model=TaskResponseSchema)
def update_task(
    task_id: int,
    updated_data: TaskUpdateSchema,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return service.update_task(task_id=task_id, task_update=updated_data, user_id=user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    service.delete_task(task_id=task_id, user_id=user.id)
    return None
