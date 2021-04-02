# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 02:51:44
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 09:18:43


import logging

import discord
from aiomysql.sa import create_engine
from discord.ext import commands

from .models import Tag, User
from .utils import get_version, load_extensions

log = logging.getLogger(__name__)


def init_events(bot):
    @bot.event
    async def on_ready():
        log.info("Mecha has started!")
        log.info("Version %s" % get_version())
        log.info("Bot Guilds: %s" % len(bot.guilds))
        log.info("Bot Users: %s" % len(list([x for x in bot.get_all_members()])))
        # print(
        #     f"Mecha is working.\nVersion: {get_version()}\nGuilds: {len(bot.guilds)}\nUsers: {len(list([x for x in bot.get_all_members()]))}"
        # )
        bot.engine = await create_engine(
            user="root",
            db="meka",
            host="127.0.0.1",
            password="",
            loop=bot.loop,
        )
        log.debug("Connected to database.")
        await User.create_table(bot.engine)
        await Tag.create_table(bot.engine)
        log.info("Ready!")

    @bot.event
    async def on_message(message):
        if bot.engine is None:
            return
        await bot.process_commands(message)
        # async with bot.engine.acquire() as conn:
        #     await conn.execute(User.table.insert().values(id=message.author.id))
        #     cursor = await conn.execute(
        #         User.table.select().where(User.table.c.id == message.author.id)
        #     )
        #     async for row in cursor:
        #         print(row.id, row.is_admin, row.is_banned)

    # @bot.event
    # async def on_command_error(ctx, e):
    #     try:
    #         e.original
    #     except:
    #         if isinstance(e, commands.CommandNotFound):
    #             await ctx.message.add_reaction("⁉")
    log.debug("Events initialized.")
