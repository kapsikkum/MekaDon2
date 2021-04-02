# @Author: kapsikkum
# @Date:   2021-04-02 13:13:49
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 13:58:05

import random

import aiohttp
import discord
from discord.ext import commands

from ..utils import Cache

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
home_page = "https://danbooru.donmai.us/"


class Client:
    def __init__(self, bot):
        self.cache = Cache(bot)

    async def get_images(self, tag):
        images = list()

        # Check if we already have images cached
        if await self.cache.get(tag):
            data = await self.cache.get(tag)
            for post in data:
                try:
                    if post["file_url"].split(".")[-1] in ["mp4", "webm"]:
                        pass
                    else:
                        images.append(
                            {
                                "file_url": post["file_url"],
                                "post_url": f"https://danbooru.donmai.us/posts/{post['id']}",
                            }
                        )
                except:
                    pass
            return images

        # Else we get them.
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://danbooru.donmai.us/posts.json",
                params={"tags": tag, "limit": 100},
                headers=headers,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await self.cache.add(tag, data, delay=500)
                    if data is not None:
                        for post in data:
                            try:
                                if post["file_url"].split(".")[-1] in [
                                    "mp4",
                                    "webm",
                                ]:
                                    pass
                                else:
                                    images.append(
                                        {
                                            "file_url": post["file_url"],
                                            "post_url": f"https://danbooru.donmai.us/posts/{post['id']}",
                                        }
                                    )
                            except:
                                pass
            data = await self.cache.get(tag)
            for post in data:
                try:
                    if post["file_url"].split(".")[-1] in ["mp4", "webm"]:
                        pass
                    else:
                        images.append(
                            {
                                "file_url": post["file_url"],
                                "post_url": f"https://danbooru.donmai.us/posts/{post['id']}",
                            }
                        )
                except:
                    pass
        return images


class Cog(commands.Cog, name="NSFW Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.danbooru = Client(bot)

    @commands.command(
        description="Get a random image from a specified tag from DanBooru. (NSFW)",
        usage="{prefix}danbooru <tags>",
        name="danbooru",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def danbooru(self, ctx, *, tag=""):
        async with ctx.typing():
            posts = await self.danbooru.get_images(tag)
            if len(posts) == 0:
                embed = discord.Embed(
                    title="No Results.", description=discord.Embed.Empty, color=0xFF0000
                )
            else:
                post = random.choice(posts)
                embed = discord.Embed(
                    title=(tag if len(tag) > 0 else "Recent Image"),
                    description=f"[Source]({post['post_url']})",
                    color=0xFF0000,
                )
                embed.set_image(url=post["file_url"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Cog(bot))
