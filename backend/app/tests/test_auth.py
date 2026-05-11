from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


client = TestClient(app)


def test_register_returns_token():
    test_email = f"user_{uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/auth/register",
        json={"name": "Test Kullanıcı", "email": test_email, "password": "secret"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["user_name"] == "Test Kullanıcı"


def test_login_returns_token():
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_get_current_user():
    login_response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "secret"})
    token = login_response.json()["access_token"]

    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["name"] == "Test Kullanıcı"
