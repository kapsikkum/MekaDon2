# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 03:01:41
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-04 07:51:16


import asyncio
import logging
import os
import random
import subprocess

import discord

log = logging.getLogger(__name__)


def get_version():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )


def get_extensions():
    e = list()
    for file in os.listdir("mecha/extensions"):
        if file.endswith(".py") and file != "__init__.py":
            e.append("mecha.extensions.%s" % file.replace(".py", ""))
    return e


def construct_post_embed(tag, posts, desc=discord.Embed.Empty):
    if len(posts) == 0:
        embed = discord.Embed(
            title="No Results.",
            description=desc,
            color=0xFF0000,
        )
    else:
        post = random.choice(posts)
        embed = discord.Embed(
            title=(tag if len(tag) > 0 else "Recent Image"),
            description="[Source](%s)" % post.post_url,
            color=0xFF0000,
        )
        embed.set_image(url=post.file_url)
    return embed


class Cache:
    def __init__(self, loop):
        self.cache = dict()
        self.loop = loop
        log.debug("Cache created")

    async def remove(self, key, duration=0):
        await asyncio.sleep(duration)
        try:
            del self.cache[key]
            log.debug("Deleted cache for key '%s'" % key)
        except:
            pass

    async def add(self, key, data, duration=50):
        self.cache[key] = data
        self.loop.create_task(self.remove(key, duration=duration))
        log.debug("Created cache for key '%s' with duration '%s'" % (key, duration))

    async def get(self, key):
        log.debug("Cache requested for key '%s'" % key)
        data = self.cache.get(key, None)
        if not data:
            log.debug("Key '%s' is not present in cache!" % key)
        return data
