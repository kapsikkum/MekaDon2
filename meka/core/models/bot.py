# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-27 15:07:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-20 08:56:44


import asyncio
import datetime
import logging

import discord
import motor.motor_asyncio
from discord.ext import commands

# from meka.core.events import init_events
from meka.core.utils import get_extensions, get_version

log = logging.getLogger(__name__)


class Bot(commands.AutoShardedBot):
    """
    Creates new instance of `Bot()` Class.
    """

    # yeah
    loaded_extensions = list()

    def __init__(self, **options):
        super().__init__(
            command_prefix=self.get_prefix,
            # help_command=None,
            intents=discord.Intents.all(),  # (messages=True, guilds=True, members=True, presences=True)
            description=f"MekaCore ({get_version()})",
            **options,
        )

        # Database shit
        self._client = motor.motor_asyncio.AsyncIOMotorClient()
        self.db = self._client.meka

        # Uptime
        self.uptime = datetime.datetime.utcnow()
        self.reconnected = False
        self.last_disconnect = None

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

    def load_extensions(self):
        log.debug("Start loading extensions")
        extensions = get_extensions()
        extensions.insert(0, "meka.core.commands")
        for ext in extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                log.error(
                    "Unable to load extension '%s'! Threw Exception '%s': %s"
                    % (ext, type(e).__name__, e)
                )
            else:
                log.info("Loaded extension '%s'" % ext)
                self.loaded_extensions.append(ext)
        log.debug("Finished loading extensions")

    def reload_extensions(self):
        log.debug("Reloading all extensions")
        extensions = get_extensions()
        for ext in extensions:
            try:
                if ext in self.loaded_extensions:
                    self.unload_extension(ext)
                    self.loaded_extensions.remove(ext)
                self.load_extension(ext)
            except Exception as e:
                log.error(
                    "Unable to reload extension '%s'! Threw Exception '%s': %s"
                    % (ext, type(e).__name__, e)
                )
            else:
                log.info("Reloaded extension '%s'" % ext)
                self.loaded_extensions.append(ext)
        log.debug("Finished reloading extensions")

    async def on_connect(self):
        self.reconnected = True

    async def on_disconnect(self):
        if self.reconnected:
            self.reconnected = False
            self.last_disconnect = datetime.datetime.utcnow()

    def total_downtime(self):
        if self.last_disconnect is None:
            return 0.0

        return (datetime.datetime.utcnow() - self.last_disconnect).total_seconds()

    # Commands
    async def on_ready(self):
        log.info("Meka has started!")
        log.info("Version %s" % get_version())
        log.info("Bot Guilds: %s" % len(self.guilds))
        log.info("Bot Users: %s" % len(list([x for x in self.get_all_members()])))

    async def on_message(self, message):
        await self.process_commands(message)

    # run
    def run(self, *args, **kwargs):
        log.info("Starting Meka...")
        # init_events(self)
        self.load_extensions()
        return super().run(*args, **kwargs)
