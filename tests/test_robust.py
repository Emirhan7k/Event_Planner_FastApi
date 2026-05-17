import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_auth_and_registration(client: AsyncClient):
    # 1. API Registration
    payload = {
        "email": "api_user@example.com",
        "username": "apiuser",
        "full_name": "API User",
        "password": "password123",
        "interests": ["tech"]
    }
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code in [200, 201], f"API Register failed: {resp.text}"
    
    # 2. Web Registration (Form)
    form_data = {
        "email": "web_user@example.com",
        "username": "webuser",
        "full_name": "Web User",
        "password": "password123",
        "interests": "music, art"
    }
    resp = await client.post("/auth/register", data=form_data)
    # Redirect to login (302/303) or success (200)
    assert resp.status_code in [200, 302, 303], f"Web Register failed: {resp.text}"

@pytest.mark.asyncio
async def test_event_and_recommendation(client: AsyncClient):
    # Login to get token
    login_data = {"email": "api_user@example.com", "password": "password123"}
    login_resp = await client.post("/api/v1/auth/login", json=login_data)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Events
    event_data = {
        "title": "AI Workshop",
        "description": "Learn artificial intelligence and tech",
        "location": "Online",
        "event_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "capacity": 50,
        "category": "tech",
        "tags": ["ai", "tech", "python"]
    }
    resp = await client.post("/api/v1/events", json=event_data, headers=headers)
    assert resp.status_code in [200, 201]
    event_id = resp.json()["id"]

    await client.post("/api/v1/events", json={
        "title": "Python Basics",
        "description": "Introduction to python coding",
        "location": "Online",
        "event_date": (datetime.now() + timedelta(days=6)).isoformat(),
        "capacity": 100,
        "category": "tech",
        "tags": ["python", "tech"]
    }, headers=headers)


    # Register for event
    resp = await client.post(f"/api/v1/registrations/{event_id}", headers=headers)
    assert resp.status_code in [200, 201]

    # Get recommendations
    resp = await client.get("/api/v1/recommendations/me", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["recommendations"]) > 0
