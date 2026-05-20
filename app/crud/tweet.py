from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Tweet
from  app.schemas.tweet import TweetIn
from app.models import User
from fastapi import HTTPException


async def create_tweet(
    db:AsyncSession,
    current_user: User,
    data: TweetIn
):
    tweet = Tweet(content=data.tweet_data, author_id=current_user.id)
    db.add(tweet)
    await db.commit()
    return tweet

async def delete_tweet(
    db: AsyncSession,
    current_user: User,
    tweet_id: int
):
    result = await db.execute(select(Tweet).where(Tweet.id == tweet_id))
    tweet = result.scalar_one_or_none()
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    if tweet.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your tweet")
    await db.delete(tweet)
    await db.commit()

async def like_tweet(
    db: AsyncSession,
    current_user: User,
    tweet_id: int
):  
    result = await db.execute(select(Tweet).where(Tweet.id == tweet_id))
    tweet = result.scalar_one_or_none()
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    tweet.likes.append(current_user)
    await db.commit()
    return True


async def unlike_tweet(
    db: AsyncSession,
    current_user: User,
    tweet_id: int
):
    result = await db.execute(select(Tweet).where(Tweet.id == tweet_id))
    tweet = result.scalar_one_or_none()
    if not tweet:
        raise HTTPException(status_code=404, detail='Tweet not found')
    tweet.likes.remove(current_user)
    await db.commit()
    return True


async def get_tweets(
    db: AsyncSession,
    current_user: User
):
    from sqlalchemy import text
    follows_result = await db.execute(
        text("SELECT following_id FROM follows WHERE follower_id = :uid"),
        {"uid": current_user.id}
    )
    following_ids = [row[0] for row in follows_result.fetchall()]
    
    if not following_ids:
        return []
    
    result = await db.execute(
        select(Tweet)
        .where(Tweet.author_id.in_(following_ids))
        .order_by(desc(Tweet.id))
    )
    return result.scalars().all()