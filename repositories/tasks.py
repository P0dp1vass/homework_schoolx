from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from models.tasks import Task
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema

class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self, user_id: int):
        return (await self.db.execute(select(Task).filter(Task.owner_id == user_id))).scalars().all()

    async def get_by_id(self, task_id: int, user_id: int):
        return (await self.db.execute(select(Task).filter(Task.id == task_id, Task.owner_id == user_id))).scalars().first()

    async def create(self, task: TaskCreateSchema, user_id: int):
        db_task = Task(**task.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update(self, db_task: Task, task_update: TaskUpdateSchema):
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def delete(self, db_task: Task):
        await self.db.delete(db_task)
        await self.db.commit()
