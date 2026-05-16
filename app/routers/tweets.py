from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.database import get_db
from app.crud.tweet import create_tweet, delete_tweet, like_tweet, unlike_tweet, get_tweets
from app.schemas.tweet import TweetIn


router = APIRouter(prefix='/api', tags=['tweets'])

@router.post('/tweets')
async def POST_tweet(
    data: TweetIn,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    tweet = await create_tweet(db, current_user, data)
    return {'result': True, 'tweet_id': tweet.id}

@router.delete('/tweets/{tweet_id}')
async def DELETE_tweet(
    tweet_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    DELETE_tweet = await delete_tweet(db, current_user, tweet_id)
    return {'result': True}

@router.post('/tweets/{tweet_id}/likes')
async def POST_like(
    tweet_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tweet_like = await like_tweet(db, current_user, tweet_id)
    return {'result': True}

@router.delete('/tweets/{tweet_id}/likes')
async def DELETE_like(
    tweet_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_like = await unlike_tweet(db, current_user, tweet_id)
    return {'result': True}

@router.get('/tweets')
async def GET_tweet(
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tweets_get = await get_tweets(db, current_user)
    return {'result': True, 'tweets': tweets_get}
    