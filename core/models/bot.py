# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-27 15:07:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-27 20:44:52


import discord
from discord.ext import commands
from core.events import init_events


class Bot(commands.AutoShardedBot):
    def __init__(self, **options):
        super().__init__(
            command_prefix="-",  # TODO change to dynamic
            help_command=None,
            intents=discord.Intents(
                messages=True, guilds=True, members=True, presences=True
            ),
            description="Mecha",
            **options
        )

    def run(self, *args, **kwargs):
        init_events(self)
        return super().run(*args, **kwargs)