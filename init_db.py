# @Author: kapsikkum
# @Date:   2021-04-02 05:58:05
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 06:01:11

import asyncio

from aiomysql.sa import create_engine

from core import Base


async def init(loop):
    engine = await create_engine(
        user="root",
        # db="meka",
        host="127.0.0.1",
        password="",
        loop=loop,
    )
    Base.metadata.create_all(engine)
    engine.close()
    await engine.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))