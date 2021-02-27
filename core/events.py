# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 02:51:44
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-27 20:32:42


import discord
from .utils import get_version


def init_events(bot):
    """Initialize the bot events.

    Args:
        bot (Client): The discord client or bot.
    """

    @bot.event
    async def on_ready():
        print(
            f"Mecha is working.\nVersion: {get_version()}\nGuilds: {len(bot.guilds)}\nUsers: {len(list([x for x in bot.get_all_members()]))}"
        )

    @bot.event
    async def on_message(message):
        print(message.content)
