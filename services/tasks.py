from fastapi import Depends
from repositories.tasks import TaskRepository
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from core.exceptions import TaskNotFoundException

class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repo = repository

    async def get_all_tasks(self, user_id: int):
        return await self.repo.get_all(user_id=user_id)

    async def get_task(self, task_id: int, user_id: int):
        task = await self.repo.get_by_id(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int):
        return await self.repo.create(task=task, user_id=user_id)

    async def update_task(self, task_id: int, task_update: TaskUpdateSchema, user_id: int):
        task = await self.get_task(task_id, user_id)
        return await self.repo.update(db_task=task, task_update=task_update)

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.get_task(task_id, user_id)
        await self.repo.delete(db_task=task)
        return {"status": "task deleted"}
