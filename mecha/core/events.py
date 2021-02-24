# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 02:51:44
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-02-25 02:52:08
import discord


def init_events(bot):
    @bot.event
    async def on_message(message):
        print(message.content)
