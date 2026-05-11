from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_events():
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()) >= 1
