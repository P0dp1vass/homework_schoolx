from fastapi import Depends
from repositories.comments import CommentRepository
from repositories.tasks import TaskRepository
from schemas.comments import CommentCreateSchema
from core.exceptions import TaskNotFoundException, CommentNotFoundException

class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository = Depends(),
        task_repo: TaskRepository = Depends()
    ):
        self.comment_repo = comment_repo
        self.task_repo = task_repo

    async def create_comment(self, task_id: int, user_id: int, comment_in: CommentCreateSchema):
        task = await self.task_repo.get_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return await self.comment_repo.create(comment_in, task_id=task_id)

    async def get_task_comments(self, task_id: int, user_id: int):
        task = await self.task_repo.get_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return await self.comment_repo.get_by_task_id(task_id)

    async def get_comment(self, comment_id: int):
        comment = await self.comment_repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)
        return comment
