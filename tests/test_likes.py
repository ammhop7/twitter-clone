import pytest
from httpx import AsyncClient
from app.models import User
from tests.conftest import async_session_maker

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def second_user():
    async with async_session_maker() as session:
        user = User(name="User2", api_key="key2")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def test_like_tweet(client: AsyncClient, test_user, second_user):
    create = await client.post(
        "/api/tweets",
        json={"tweet_data": "Like this!", "tweet_media_ids": []},
        headers={"api-key": "testkey"},
    )
    tweet_id = create.json()["tweet_id"]

    response = await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "key2"},
    )
    assert response.status_code == 200
    assert response.json()["result"] is True


async def test_unlike_tweet(client: AsyncClient, test_user, second_user):
    create = await client.post(
        "/api/tweets",
        json={"tweet_data": "Unlike this!", "tweet_media_ids": []},
        headers={"api-key": "testkey"},
    )
    tweet_id = create.json()["tweet_id"]

    await client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "key2"},
    )

    response = await client.delete(
        f"/api/tweets/{tweet_id}/likes",
        headers={"api-key": "key2"},
    )
    assert response.status_code == 200
    assert response.json()["result"] is True


async def test_like_nonexistent_tweet(client: AsyncClient, test_user):
    response = await client.post(
        "/api/tweets/99999/likes",
        headers={"api-key": "testkey"},
    )
    assert response.status_code == 404
