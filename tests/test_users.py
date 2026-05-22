import pytest
from httpx import AsyncClient
from app.models import User
from tests.conftest import async_session_maker

pytestmark = pytest.mark.asyncio


async def test_get_me(client: AsyncClient, test_user):
    response = await client.get("/api/users/me", headers={"api-key": "testkey"})
    print(response.json())
    assert response.status_code == 200, response.text
    assert response.json()["result"] is True
    assert response.json()["user"]["name"] == "TestUser"


async def test_get_user_by_id(client: AsyncClient, test_user):
    response = await client.get(
        f"/api/users/{test_user.id}", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True


async def test_follow_unfollow(client: AsyncClient, test_user):
    
    async with async_session_maker() as session:
        user2 = User(name="User2", api_key="key2")
        session.add(user2)
        await session.commit()
        user2_id = user2.id

    response = await client.post(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

    response = await client.delete(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
