from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=True)
    tweet = relationship('Tweet', back_populates='attachments')