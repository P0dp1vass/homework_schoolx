from fastapi import Depends
from repositories.tasks import TaskRepository
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema
from core.exceptions import TaskNotFoundException

class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repo = repository

    def get_all_tasks(self, user_id: int):
        return self.repo.get_all(user_id=user_id)

    def get_task(self, task_id: int, user_id: int):
        task = self.repo.get_by_id(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return task

    def create_task(self, task: TaskCreateSchema, user_id: int):
        return self.repo.create(task=task, user_id=user_id)

    def update_task(self, task_id: int, task_update: TaskUpdateSchema, user_id: int):
        task = self.get_task(task_id, user_id)
        return self.repo.update(db_task=task, task_update=task_update)

    def delete_task(self, task_id: int, user_id: int):
        task = self.get_task(task_id, user_id)
        self.repo.delete(db_task=task)
        return {"status": "task deleted"}
