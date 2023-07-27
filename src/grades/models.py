import enum

from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, UniqueConstraint

metadata = MetaData()


class Status(enum.Enum):
    like = 1
    dislike = 0


grade = Table(
    "grade",
    metadata,
    Column("id", Integer, primary_key=True),
    Column('state', enum.Enum(Status)),
    Column("user_id",
           Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("post_id",
           Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True),
    UniqueConstraint("user_id", "post_id"),
)
