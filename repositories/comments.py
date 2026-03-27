from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.comments import Comment
from schemas.comments import CommentCreateSchema

class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, comment_in: CommentCreateSchema, task_id: int) -> Comment:
        db_comment = Comment(text=comment_in.text, task_id=task_id)
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def get_by_task_id(self, task_id: int) -> list[Comment]:
        return self.db.query(Comment).filter(Comment.task_id == task_id).all()

    def get_by_id(self, comment_id: int) -> Comment | None:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()
