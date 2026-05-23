from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import tweets, users, media
import os

app = FastAPI(title='Twitter Clone')

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(media.router)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get('/')
async def root():
    return {'message': 'ok'}
