from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_recommendations_are_ranked():
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    scores = [item["score"] for item in response.json()]
    assert scores == sorted(scores, reverse=True)
