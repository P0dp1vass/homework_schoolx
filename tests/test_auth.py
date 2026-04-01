import pytest
@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "StrongPassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "is_active" in data

@pytest.mark.asyncio
async def test_register_duplicate(client):
    user_data = {"email": "duplicate@example.com", "password": "StrongPassword123"}
    await client.post("/auth/register", json=user_data)
    
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "USER_ALREADY_EXISTS"

@pytest.mark.asyncio
async def test_login_success(client):
    user_data = {"email": "loginuser@example.com", "password": "StrongPassword123"}
    await client.post("/auth/register", json=user_data)
    
    response = await client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_password(client):
    user_data = {"email": "loginuser@example.com", "password": "StrongPassword123"}
    await client.post("/auth/register", json=user_data)
    
    wrong_data = {"email": "loginuser@example.com", "password": "WrongPassword"}
    response = await client.post("/auth/login", json=wrong_data)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

@pytest.mark.asyncio
async def test_login_invalid_email(client):
    wrong_data = {"email": "notfound@example.com", "password": "WrongPassword"}
    response = await client.post("/auth/login", json=wrong_data)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"
