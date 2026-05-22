from fastapi import FastAPI
from app.routers import tweets, users, media

app = FastAPI(title="Twitter Clone")

app.include_router(tweets.router)
app.include_router(users.router)
app.include_router(media.router)


@app.get("/")
async def root():
    return {"message": "ok"}
