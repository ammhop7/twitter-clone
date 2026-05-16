from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.database import get_db
from app.crud.user import get_user_by_id, follow_user, unfollow_user
from app.schemas.user import UserOut

router = APIRouter(prefix='/api', tags=['users'])

@router.get('/users/me')
async def GET_me(
    current_user = Depends(get_current_user)
):
    return {'result': True, 'user': UserOut.model_validate(current_user)}

@router.get('/users/{user_id}')
async def GET_users(
     user_id: int,
    db = Depends(get_db)
):
    get_users = await get_user_by_id(db, user_id)
    return {'result': True, 'user': UserOut.model_validate(get_users)}

@router.post('/users/{user_id}/follow')
async def POST_follow(
    user_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post_follow = await follow_user(db, current_user, user_id)
    return {'result': True}

@router.delete('/users/{user_id}/follow')
async def DELETE_follow(
    user_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_follow = await unfollow_user(db, current_user, user_id)
    return {'result': True}