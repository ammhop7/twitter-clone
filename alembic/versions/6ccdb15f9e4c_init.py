"""init

Revision ID: 6ccdb15f9e4c
Revises:
Create Date: 2026-05-16 23:46:08.392225

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6ccdb15f9e4c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.Column("tweet_id", sa.Integer(), sa.ForeignKey("tweets.id"), nullable=True),
    )
    op.create_table(
        "follows",
        sa.Column(
            "follower_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True
        ),
        sa.Column(
            "following_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True
        ),
    )
    op.create_table(
        "likes",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column(
            "tweet_id", sa.Integer(), sa.ForeignKey("tweets.id"), primary_key=True
        ),
    )


def downgrade() -> None:
    op.drop_table("likes")
    op.drop_table("follows")
    op.drop_table("media")
    op.drop_table("tweets")
    op.drop_table("users")
