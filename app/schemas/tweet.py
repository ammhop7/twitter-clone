from pydantic import BaseModel
from app.schemas.user import UserShort


class LikeOut(BaseModel):
    model_config = {"from_attributes": True}

    user_id: int
    name: str


class TweetOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    content: str
    attachments: list[str]
    author: UserShort
    likes: list[LikeOut]


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None = None
