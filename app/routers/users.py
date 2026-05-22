from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from app.dependencies import get_current_user
from app.database import get_db
from app.crud.user import get_user_by_id, follow_user, unfollow_user

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/users/me")
async def GET_me(current_user=Depends(get_current_user), db=Depends(get_db)):
    followers_result = await db.execute(
        text(
            "SELECT u.id, u.name FROM users u JOIN follows f ON f.follower_id = u.id WHERE f.following_id = :uid"
        ),
        {"uid": current_user.id},
    )
    following_result = await db.execute(
        text(
            "SELECT u.id, u.name FROM users u JOIN follows f ON f.following_id = u.id WHERE f.follower_id = :uid"
        ),
        {"uid": current_user.id},
    )
    followers = [{"id": r[0], "name": r[1]} for r in followers_result.fetchall()]
    following = [{"id": r[0], "name": r[1]} for r in following_result.fetchall()]
    return {
        "result": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "followers": followers,
            "following": following,
        },
    }


@router.get("/users/{user_id}")
async def GET_user(user_id: int, db=Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers_result = await db.execute(
        text(
            "SELECT u.id, u.name FROM users u JOIN follows f ON f.follower_id = u.id WHERE f.following_id = :uid"
        ),
        {"uid": user_id},
    )
    following_result = await db.execute(
        text(
            "SELECT u.id, u.name FROM users u JOIN follows f ON f.following_id = u.id WHERE f.follower_id = :uid"
        ),
        {"uid": user_id},
    )
    followers = [{"id": r[0], "name": r[1]} for r in followers_result.fetchall()]
    following = [{"id": r[0], "name": r[1]} for r in following_result.fetchall()]
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": followers,
            "following": following,
        },
    }


@router.post("/users/{user_id}/follow")
async def POST_follow(
    user_id: int, db=Depends(get_db), current_user=Depends(get_current_user)
):
    await follow_user(db, current_user, user_id)
    return {"result": True}


@router.delete("/users/{user_id}/follow")
async def DELETE_follow(
    user_id: int, db=Depends(get_db), current_user=Depends(get_current_user)
):
    await unfollow_user(db, current_user, user_id)
    return {"result": True}
