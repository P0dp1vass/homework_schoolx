from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User
from schemas.users import UserRegistrationSchema
from core.database import get_db

class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        return (await self.db.execute(select(User).filter(User.email == email))).scalars().first()

    async def create(self, user_in: UserRegistrationSchema, hashed_password: str) -> User:
        db_user = User(email=user_in.email, hashed_password=hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
