from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("tweet_id", ForeignKey("tweets.id"), primary_key=True),
)


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="tweets", lazy="selectin")
    likes = relationship("User", secondary=likes, lazy="selectin")
    attachments = relationship("Media", back_populates="tweet", lazy="selectin")
