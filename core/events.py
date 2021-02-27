# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 02:51:44
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-25 03:18:17


import discord
from .utils import get_version


def init_events(bot):
    @bot.event
    async def on_ready():
        print(f"Mecha is working.\nVersion: {get_version()}")

    @bot.event
    async def on_message(message):
        print(message.content)
