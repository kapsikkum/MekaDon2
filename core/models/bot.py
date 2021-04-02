# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-27 15:07:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 09:09:22


import asyncio
import logging

import discord
from core.events import init_events
from discord.ext import commands

from ..utils import get_version, load_extensions

log = logging.getLogger(__name__)


class Bot(commands.AutoShardedBot):
    """
    Creates new instance of `Bot()` Class.
    """

    uptime = None

    def __init__(self, **options):
        self.engine = None
        super().__init__(
            command_prefix=self.get_prefix,
            help_command=None,
            intents=discord.Intents(
                messages=True, guilds=True, members=True, presences=True
            ),
            description=f"MechaCore ({get_version()})",
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
        log.info("Starting Mecha...")
        init_events(self)
        load_extensions(self)
        return super().run(*args, **kwargs)
