# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-28 16:47:09
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 15:07:40

from . import client, db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User:
    def __init__(self) -> None:
        pass

    @classmethod
    async def get(self, id):
        document = await db.user.find_one({"id": id})
        return document
