from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

follows = Table(
    "follows",
    Base.metadata,
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
    Column("following_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    followers = relationship(
        "User",
        secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.following_id == id),
        overlaps="following",
        lazy="selectin",
    )
    following = relationship(
        "User",
        secondary=follows,
        primaryjoin=(follows.c.following_id == id),
        secondaryjoin=(follows.c.follower_id == id),
        overlaps="followers",
        lazy="selectin",
    )
    tweets = relationship("Tweet", back_populates="author", lazy="selectin")
