from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

async def get_user_by_id(
    db: AsyncSession,
    user_id: int
    ) -> None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def follow_user(
    db: AsyncSession,
    current_user: User,
    user_id: int
):
    user = await get_user_by_id(db, user_id)
    current_user.following.append(user)
    
    await db.commit()
    return True


async def unfollow_user(
    db: AsyncSession,
    current_user: User,
    user_id: int
):
    user = await get_user_by_id(db, user_id)
    current_user.following.remove(user)
    
    await db.commit()
    return True

