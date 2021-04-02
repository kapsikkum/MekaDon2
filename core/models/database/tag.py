# @Author: kapsikkum
# @Date:   2021-04-02 05:40:13
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 07:21:03

import sqlalchemy as db

from . import metadata


class Tag:
    table = db.Table(
        "tags",
        metadata,
        db.Column("id", db.Integer, primary_key=True),
        db.Column("content", db.String(2000), nullable=False),
        db.Column("owner", db.Integer, nullable=False),
        db.Column("created_at", db.DateTime, nullable=False),
    )

    @classmethod
    async def create_table(self, engine):
        async with engine.acquire() as conn:
            await conn.execute("DROP TABLE IF EXISTS tags")
            await conn.execute(
                """CREATE TABLE IF NOT EXISTS tags (id BIGINT PRIMARY KEY, content VARCHAR(2000), owner INT, created_at DATETIME)"""
            )

    def __init__(self, id, content, owner, created_at):
        self.id = id
        self.content = content
        self.owner = owner
        self.created_at = created_at


# tags = db.Table(
#     "tags",
#     metadata,
#     db.Column("id", db.Integer, primary_key=True),
#     db.Column("content", db.String(2000), nullable=False),
#     db.Column("owner", db.Integer, db.ForeignKey("users.id"), nullable=False),
#     db.Column("created_at", db.DateTime, nullable=False),
# )


# class Tag(Base):
#     __tablename__ = "tags"

#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(2000), nullable=False)
#     owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False)

#     def __repr__(self):
#         return "<Tag(id='%s', owner='%s', created_at='%s', content='%s')>" % (
#             self.id,
#             self.owner,
#             self.created_at,
#             self.content,
#         )
