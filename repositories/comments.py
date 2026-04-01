from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from models.comments import Comment
from schemas.comments import CommentCreateSchema

class CommentRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, comment_in: CommentCreateSchema, task_id: int) -> Comment:
        db_comment = Comment(text=comment_in.text, task_id=task_id)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment

    async def get_by_task_id(self, task_id: int) -> list[Comment]:
        return (await self.db.execute(select(Comment).filter(Comment.task_id == task_id))).scalars().all()

    async def get_by_id(self, comment_id: int) -> Comment | None:
        return (await self.db.execute(select(Comment).filter(Comment.id == comment_id))).scalars().first()
