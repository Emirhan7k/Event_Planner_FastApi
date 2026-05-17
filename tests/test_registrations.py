import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_event_registration(client: AsyncClient):
    # Register & Login
    reg_payload = {
        "email": "reg@example.com",
        "username": "reguser",
        "password": "password123",
        "full_name": "Reg User"
    }
    reg_resp = await client.post("/api/v1/auth/register", json=reg_payload)
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create an event to register for
    event_payload = {
        "title": "Reg Event",
        "description": "Desc",
        "location": "Loc",
        "event_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "capacity": 10,
        "category": "Music"
    }
    event_resp = await client.post("/api/v1/events", json=event_payload, headers=headers)
    event_id = event_resp.json()["id"]

    # Register for the event
    response = await client.post(f"/api/v1/registrations/{event_id}", headers=headers)
    assert response.status_code in [200, 201]
    assert response.json()["event_id"] == event_id
    assert response.json()["status"] == "confirmed"
