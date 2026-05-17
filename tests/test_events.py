import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_event(client: AsyncClient):
    # Register & Login to get token
    reg_payload = {
        "email": "event@example.com",
        "username": "eventuser",
        "password": "password123",
        "full_name": "Event User"
    }
    reg_resp = await client.post("/api/v1/auth/register", json=reg_payload)
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create event
    event_payload = {
        "title": "Test Event",
        "description": "This is a test event description",
        "location": "Test City",
        "event_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "capacity": 50,
        "category": "Tech",
        "tags": ["pytest", "fastapi"]
    }
    response = await client.post("/api/v1/events", json=event_payload, headers=headers)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == "Test Event"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_get_events(client: AsyncClient):
    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    assert "items" in response.json()
