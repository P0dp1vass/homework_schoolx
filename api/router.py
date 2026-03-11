from fastapi import APIRouter, HTTPException
from typing import List
from schemas.tasks import BaseTask, CreateTask, EditTask
import services.tasks as task_service_module

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# используем класс сервиса (он хранит общий список `tasks` в модуле)
service = task_service_module.TaskService()


@router.post("/", response_model=BaseTask, status_code=201)
def create_task(task: CreateTask):
    result = service.add_task(task)
    if isinstance(result, dict):
        # сервис возвращает dict с причиной при ошибке
        raise HTTPException(status_code=400, detail=result.get("reason"))
    return result


@router.get("/", response_model=List[BaseTask])
def get_all_tasks():
    return service.get_all_tasks()


@router.get("/{task_name}", response_model=BaseTask)
def get_task(task_name: str):
    for t in service.user_tasks:
        if t.name == task_name:
            return t
    raise HTTPException(status_code=404, detail="No task")


@router.patch("/{task_name}", response_model=BaseTask)
def update_task(task_name: str, updated_data: EditTask):
    result = service.edit_task(task_name, updated_data)
    if isinstance(result, dict):
        raise HTTPException(status_code=400, detail=result.get("reason"))
    return result


@router.delete("/{task_name}", status_code=204)
def delete_task(task_name: str):
    result = service.delete_task(task_name)
    if result.get("status") != "task deleted":
        raise HTTPException(status_code=404, detail=result.get("reason"))
    return None