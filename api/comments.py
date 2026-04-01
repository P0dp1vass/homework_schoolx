from fastapi import APIRouter, Depends, status
from typing import List

from schemas.comments import CommentCreateSchema, CommentResponseSchema
from services.comments import CommentService
from dependency import get_current_user
from models.users import User

router = APIRouter(prefix="/tasks", tags=["comments"])

@router.post("/{task_id}/comments", response_model=CommentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: int,
    comment_in: CommentCreateSchema,
    service: CommentService = Depends(),
    current_user: User = Depends(get_current_user)
):
    return await service.create_comment(task_id=task_id, user_id=current_user.id, comment_in=comment_in)

@router.get("/{task_id}/comments", response_model=List[CommentResponseSchema])
async def get_task_comments(
    task_id: int,
    service: CommentService = Depends(),
    current_user: User = Depends(get_current_user)
):
    return await service.get_task_comments(task_id=task_id, user_id=current_user.id)
