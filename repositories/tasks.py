from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.tasks import Task
from schemas.tasks import TaskCreateSchema, TaskUpdateSchema

class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, user_id: int):
        return self.db.query(Task).filter(Task.owner_id == user_id).all()

    def get_by_id(self, task_id: int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()

    def create(self, task: TaskCreateSchema, user_id: int):
        db_task = Task(**task.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update(self, db_task: Task, task_update: TaskUpdateSchema):
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, db_task: Task):
        self.db.delete(db_task)
        self.db.commit()
