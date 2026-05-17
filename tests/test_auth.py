import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    payload = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "interests": ["tech", "music"]
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # First register
    reg_payload = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "password123",
        "full_name": "Login User"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    # Then login
    login_payload = {
        "email": "login@example.com",
        "password": "password123"
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
