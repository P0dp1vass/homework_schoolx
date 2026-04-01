import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.database import Base, get_db
from models import User, Task
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        pass

@pytest_asyncio.fixture
async def db(db_engine):
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def auth_token(client):
    user_data = {"email": "testuser@example.com", "password": "StrongPassword123"}
    await client.post("/auth/register", json=user_data)
    response = await client.post("/auth/login", json=user_data)
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def second_auth_token(client):
    user_data = {"email": "seconduser@example.com", "password": "StrongPassword123"}
    await client.post("/auth/register", json=user_data)
    response = await client.post("/auth/login", json=user_data)
    return response.json()["access_token"]
