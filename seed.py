import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app.models.user import User
from app.config import settings


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    session = async_sessionmaker(engine, class_=AsyncSession)
    async with session() as s:
        users = [
            User(name="Test", api_key="test"),
            User(name="Test2", api_key="test2"),
        ]
        s.add_all(users)
        await s.flush()
        await s.execute(
            text("INSERT INTO follows VALUES (:a, :b)"),
            {"a": users[0].id, "b": users[1].id},
        )
        await s.commit()
        print("Done!")


asyncio.run(seed())
