# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-27 15:07:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 14:55:28


import asyncio

import discord
from core.events import init_events
from discord.ext import commands

from ..utils import get_version


class Bot(commands.AutoShardedBot):
    """
    Creates new instance of `Bot()` Class.
    """

    uptime = None

    def __init__(self, **options):
        self.pool = None
        super().__init__(
            command_prefix=self.get_prefix,
            help_command=None,
            intents=discord.Intents(
                messages=True, guilds=True, members=True, presences=True
            ),
            description="Mecha",
            **options,
        )

    async def get_prefix(self, message):
        return commands.when_mentioned_or("-")(self, message)
        if message.guild is None:
            return commands.when_mentioned_or("-")(self, message)
        elif str(message.guild.id) in prefixes:
            return commands.when_mentioned_or(prefixes[str(message.guild.id)])(
                self, message
            )
        else:
            return commands.when_mentioned_or(core.prefix)(self, message)

    def run(self, *args, **kwargs):
        init_events(self)
        return super().run(*args, **kwargs)
