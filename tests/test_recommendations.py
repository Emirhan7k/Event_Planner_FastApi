import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_recommendations(client: AsyncClient):
    # Create user with 'tech' interest
    reg_payload = {
        "email": "ai@example.com",
        "username": "aiuser",
        "password": "password123",
        "full_name": "AI User",
        "interests": ["tech"]
    }
    reg_resp = await client.post("/api/v1/auth/register", json=reg_payload)
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create one tech event and one music event
    await client.post("/api/v1/events", json={
        "title": "Python Workshop",
        "description": "Learn python coding",
        "location": "Online",
        "event_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "capacity": 100,
        "category": "Tech",
        "tags": ["python", "tech", "coding"]
    }, headers=headers)

    await client.post("/api/v1/events", json={
        "title": "Jazz Night",
        "description": "Live jazz music",
        "location": "Club",
        "event_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "capacity": 50,
        "category": "Music",
        "tags": ["jazz", "music"]
    }, headers=headers)

    # Get recommendations
    response = await client.get("/api/v1/recommendations", headers=headers)
    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    
    # Python workshop should have a higher score than Jazz night for a 'tech' interested user
    if len(recommendations) >= 2:
        # Check if Python is first or has higher score
        python_event = next(e for e in recommendations if "Python" in e["title"])
        jazz_event = next(e for e in recommendations if "Jazz" in e["title"])
        assert python_event["score"] >= jazz_event["score"]
