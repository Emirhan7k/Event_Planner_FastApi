from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_returns_token():
    response = client.post("/api/auth/login", json={"email": "ali@example.com", "password": "secret"})
    assert response.status_code == 200
    assert response.json()["access_token"]
