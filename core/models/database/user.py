# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-28 16:47:09
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 07:18:43

import sqlalchemy as db

from . import metadata


class User:
    table = db.Table(
        "users",
        metadata,
        db.Column("id", db.Integer, primary_key=True, autoincrement=False),
        db.Column("money", db.Float, nullable=False, default=0),
        db.Column("is_admin", db.Boolean, nullable=False, default=False),
        db.Column("is_banned", db.Boolean, nullable=False, default=False),
    )

    @classmethod
    async def create_table(self, engine):
        async with engine.acquire() as conn:
            await conn.execute("DROP TABLE IF EXISTS users")
            await conn.execute(
                """CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, money FLOAT, is_admin BOOL, is_banned BOOL)"""
            )

    def __init__(self, id, money, is_admin, is_banned):
        self.id = id
        self.money = money
        self.is_admin = is_admin
        self.is_banned = is_banned


# users = db.Table(
#     "users",
#     metadata,
#     db.Column("id", db.Integer, primary_key=True, autoincrement=False),
#     db.Column("is_admin", db.Boolean, nullable=False, default=False),
#     db.Column("is_banned", db.Boolean, nullable=False, default=False),
# )


# async def create_users(engine):
#     async with engine.acquire() as conn:
#         await conn.execute(
#             """CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, is_admin bool, is_banned bool)"""
#         )


# class User(Base):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=False)
#     is_admin = db.Column(db.Boolean, nullable=False, default=False)
#     is_banned = db.Column(db.Boolean, nullable=False, default=False)

#     def __repr__(self):
#         return "<User(id='%s', is_admin='%s', is_banned='%s')>" % (
#             self.id,
#             self.is_admin,
#             self.is_banned,
#         )
