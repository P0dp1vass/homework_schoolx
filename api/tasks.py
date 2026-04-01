from fastapi import UploadFile, File
from core.minio_client import upload_file_to_minio
from fastapi import APIRouter, status, Depends
from typing import List

from dependency import get_current_user
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from services.tasks import TaskService
from models.users import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreateSchema,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return await service.create_task(task=task, user_id=user.id)

@router.get("/", response_model=List[TaskResponseSchema])
async def get_all_tasks(
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return await service.get_all_tasks(user_id=user.id)

@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(
    task_id: int,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return await service.get_task(task_id=task_id, user_id=user.id)

@router.patch("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int,
    updated_data: TaskUpdateSchema,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    return await service.update_task(task_id=task_id, task_update=updated_data, user_id=user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(),
    user: User = Depends(get_current_user)
):
    await service.delete_task(task_id=task_id, user_id=user.id)
    return None

@router.post("/{task_id}/upload-avatar")
async def upload_task_avatar(
    task_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user)
):
    # Synchronously read to wrap length (since Minio wrapper uses sync read pattern usually or to_thread).
    # Since fastAPI UploadFile gives async read and sync read, we use file.file (SpooledTemporaryFile)
    url = await upload_file_to_minio(
        bucket_name="task-avatars",
        object_name=f"{task_id}_{file.filename}",
        data=file.file,
        length=file.size,
        content_type=file.content_type
    )
    return {"url": url}
