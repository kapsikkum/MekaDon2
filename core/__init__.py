# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 02:12:03
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-25 03:16:49
import discord
from discord.ext import commands

bot = commands.AutoShardedBot(
    command_prefix="-",  # TODO change to dynamic
    help_command=None,
    intents=discord.Intents(messages=True, guilds=True, members=True, presences=True),
)
