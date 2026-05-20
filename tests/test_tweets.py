import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_tweet(client: AsyncClient, test_user):
    response = await client.post(
        "/api/tweets",
        json={"tweet_data": "Hello world!"},
        headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert "tweet_id" in response.json()


async def test_get_tweets(client: AsyncClient, test_user):
    response = await client.get(
        "/api/tweets",
        headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert "tweets" in response.json()


async def test_delete_tweet(client: AsyncClient, test_user):
    create = await client.post(
        "/api/tweets",
        json={"tweet_data": "To be deleted"},
        headers={"api-key": "testkey"}
    )
    tweet_id = create.json()["tweet_id"]
    response = await client.delete(
        f"/api/tweets/{tweet_id}",
        headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True