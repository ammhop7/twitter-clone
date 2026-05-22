import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_no_api_key(client: AsyncClient):
    # FastAPI возвращает 422 когда обязательный заголовок отсутствует
    response = await client.get("/api/tweets")
    assert response.status_code == 422


async def test_wrong_api_key(client: AsyncClient):
    response = await client.get(
        "/api/tweets",
        headers={"api-key": "wrong_key"},
    )
    assert response.status_code == 403


async def test_get_nonexistent_user(client: AsyncClient, test_user):
    response = await client.get(
        "/api/users/99999",
        headers={"api-key": "testkey"},
    )
    assert response.status_code == 404


async def test_delete_tweet_not_owner(client: AsyncClient, test_user):
    from app.models import User
    from tests.conftest import async_session_maker

    async with async_session_maker() as session:
        other = User(name="Other", api_key="otherkey")
        session.add(other)
        await session.commit()

    create = await client.post(
        "/api/tweets",
        json={"tweet_data": "Owner's tweet", "tweet_media_ids": []},
        headers={"api-key": "testkey"},
    )
    tweet_id = create.json()["tweet_id"]

    response = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": "otherkey"},
    )
    assert response.status_code == 403


async def test_delete_nonexistent_tweet(client: AsyncClient, test_user):
    response = await client.delete(
        "/api/tweets/99999",
        headers={"api-key": "testkey"},
    )
    assert response.status_code == 404


async def test_follow_nonexistent_user(client: AsyncClient, test_user):
    response = await client.post(
        "/api/users/99999/follow",
        headers={"api-key": "testkey"},
    )
    assert response.status_code == 404
