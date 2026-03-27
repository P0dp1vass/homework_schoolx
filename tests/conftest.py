import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from core.database import Base, get_db

# Важно импортировать модели до вызова Base.metadata.create_all()
import models.users
import models.tasks
import models.comments

# Используем in-memory базу SQLite для быстрых, изолированных тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,  # Включаем логирование всех SQL-запросов
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Очищаем базу после каждого теста, чтобы они не зависели друг от друга
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Подменяем зависимость вызова базы данных
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Сбрасываем подмену после теста
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_token(client):
    # Регистрируем пользователя
    client.post(
        "/auth/register",
        json={"email": "testuser@example.com", "password": "TestPassword123!"}
    )
    # Авторизуемся и получаем токен
    response = client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "TestPassword123!"}
    )
    token = response.json().get("access_token")
    return token

@pytest.fixture(scope="function")
def second_auth_token(client):
    client.post(
        "/auth/register",
        json={"email": "second@example.com", "password": "TestPassword123!"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "second@example.com", "password": "TestPassword123!"}
    )
    return response.json().get("access_token")
