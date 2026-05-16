from fastapi import APIRouter, Depends, UploadFile, File
from app.dependencies import get_current_user
from app.database import get_db
from app.models import Media
import aiofiles
import os

router = APIRouter(prefix='/api', tags=['media'])

@router.post('/medias')
async def upload_media(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    os.makedirs('uploads', exist_ok=True)
    file_path = f'uploads/{file.filename}'

    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    media = Media(file_path=file_path)
    db.add(media)
    await db.commit()
    return {'result': True, 'media_id': media.id}