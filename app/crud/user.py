from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models import User


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def follow_user(db: AsyncSession, current_user: User, user_id: int):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
        select(User)
        .where(User.id == current_user.id)
        .options(selectinload(User.following))
    )
    me = result.scalar_one()
    if user not in me.following:
        me.following.append(user)
    await db.commit()
    return True


async def unfollow_user(db: AsyncSession, current_user: User, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
        select(User)
        .where(User.id == current_user.id)
        .options(selectinload(User.following))
    )
    me = result.scalar_one()
    if user in me.following:
        me.following.remove(user)
    await db.commit()
    return True
