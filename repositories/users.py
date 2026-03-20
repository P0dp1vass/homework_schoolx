from fastapi import Depends
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserRegistrationSchema
from core.database import get_db

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_in: UserRegistrationSchema, hashed_password: str) -> User:
        db_user = User(email=user_in.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
