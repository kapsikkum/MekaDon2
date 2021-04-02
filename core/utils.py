# -*- coding: utf-8 -*-
# @Author: kapsikkum
# @Date:   2021-02-25 03:01:41
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 13:20:01


import asyncio
import logging
import os
import subprocess

log = logging.getLogger(__name__)


def get_version():
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode()
    )


def load_extensions(bot):
    log.debug("Start loading extensions")
    for file in os.listdir("core/extensions"):
        if file.endswith(".py") and file != "__init__.py":
            try:
                bot.load_extension("core.extensions.%s" % file.replace(".py", ""))
                log.info(
                    "Loaded extension 'core.extensions.%s'" % file.replace(".py", "")
                )
            except Exception as e:
                log.error(
                    "Unable to load extension 'core.extensions.%s', Exception: %s"
                    % (file.replace(".py", ""), e)
                )
    log.debug("Finished loading extensions")


class Cache:
    def __init__(self, bot):
        self.cache = dict()
        self.loop = bot.loop

    @asyncio.coroutine
    async def remove(self, key, delay=0):
        await asyncio.sleep(delay)
        try:
            del self.cache[key]
        except:
            pass

    @asyncio.coroutine
    async def add(self, key, data, delay=50):
        self.cache[key] = data
        self.loop.create_task(self.remove(key, delay=delay))

    @asyncio.coroutine
    async def get(self, key):
        return self.cache.get(key, None)
