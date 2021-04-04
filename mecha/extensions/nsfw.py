# @Author: kapsikkum
# @Date:   2021-04-02 13:13:49
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-04 07:57:36
# TODO optimize a bit more!

import logging
import random

import aiohttp
import discord
from discord.ext import commands

from mecha.core import BooruPost, Cache
from mecha.core.utils import construct_post_embed

log = logging.getLogger(__name__)


class GenericClient:
    """
    Based!
    """

    def __init__(
        self,
        bot,
        api_url=None,
        post_url=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        },
    ):
        self.cache = Cache(bot.loop)
        self.api_url = api_url
        self.post_url = post_url
        self.headers = headers
        log.debug("%s created with api_url='%s'" % (self.__class__.__name__, api_url))

    async def get_posts(self, tag):
        raise NotImplementedError


class DanbooruClient(GenericClient):
    """
    Most Danbooru-like sites use this.
    """

    def __init__(
        self,
        bot,
        api_url="https://danbooru.donmai.us/posts.json",
        post_url="https://danbooru.donmai.us/posts/{id}",
    ):
        super().__init__(bot, api_url, post_url)

    async def get_posts(self, tag):
        posts = list()

        # Check if we already have posts cached
        data = await self.cache.get(tag)
        if data:
            log.debug(
                "Retrieved %s posts from cache with tag(s) '%s'" % (len(data), tag)
            )
            return data

        # Else we get them.
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_url,
                params={"tags": tag, "limit": 100},
                headers=self.headers,
            ) as response:
                if response.ok:
                    data = await response.json()
                    log.debug("Found %s posts with tag(s) '%s'" % (len(data), tag))
                    for post in data:
                        try:
                            post["file_url"]
                            post["id"]
                        except Exception as e:
                            log.warning("A post was missing %s!" % str(e))
                            continue
                        if not post["file_url"].split(".")[-1] in [
                            "mp4",
                            "webm",
                        ]:
                            posts.append(
                                BooruPost(
                                    post["file_url"],
                                    self.post_url.format(id=post["id"]),
                                )
                            )
                    await self.cache.add(tag, posts, duration=500)
                    return posts


class GelbooruClient(GenericClient):
    """
    Most Gelbooru based sites use this. (All of them lmfao)
    """

    def __init__(
        self,
        bot,
        api_url="https://gelbooru.com/index.php",
        post_url="https://gelbooru.com/index.php?page=post&s=view&id={id}",
        old=False,
    ):
        # this stuff is for the sites that use older versions of gelbooru.
        self.old = old

        super().__init__(bot, api_url, post_url)

    async def get_posts(self, tag):
        posts = list()

        # Check if we already have posts cached
        data = await self.cache.get(tag)
        if data:
            log.debug(
                "Retrieved %s posts from cache with tag(s) '%s'" % (len(data), tag)
            )
            return data

        # Else we get them.
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_url,
                params={
                    "page": "dapi",
                    "s": "post",
                    "q": "index",
                    "json": 1,
                    "tags": tag,
                },
                headers=self.headers,
            ) as response:
                if response.ok:
                    data = await response.json(
                        content_type=None  # Older gelbooru sites have the mimetype as text/html :rolling_eyes:
                    )
                    log.debug("Found %s posts with tag(s) '%s'" % (len(data), tag))
                    for post in data:
                        if not self.old:
                            # new gelbooru (gelbooru itself)
                            try:
                                post["file_url"]
                                post["id"]
                            except Exception as e:
                                log.warning("A post was missing %s!" % str(e))
                                continue
                            if not post["file_url"].split(".")[-1] in [
                                "mp4",
                                "webm",
                            ]:
                                posts.append(
                                    BooruPost(
                                        post["file_url"],
                                        self.post_url.format(id=post["id"]),
                                    )
                                )
                        else:
                            # older gelbooru
                            try:
                                post["image"]
                                post["id"]
                            except Exception as e:
                                log.warning("A post was missing %s!" % str(e))
                                continue
                            if not post["image"].split(".")[-1] in [
                                "mp4",
                                "webm",
                            ]:
                                posts.append(
                                    BooruPost(
                                        "%s/images/%s/%s"
                                        % (
                                            self.post_url,
                                            post["directory"],
                                            post["image"],
                                        ),
                                        "%s/index.php?page=post&s=view&id=%s"
                                        % (self.post_url, post["id"]),
                                    )
                                )

                    await self.cache.add(tag, posts, duration=500)
                    return posts


class E621Client(DanbooruClient):
    """
    Customized Danbooru client for the furry site e621
    """

    def __init__(self, bot):
        super().__init__(
            bot,
            api_url="https://e621.net/posts.json",
            post_url="https://e621.net/posts/{id}",
        )

    async def get_posts(self, tag):
        posts = list()

        # Check if we already have posts cached
        data = await self.cache.get(tag)
        if data:
            log.debug(
                "Retrieved %s posts from cache with tag(s) '%s'" % (len(data), tag)
            )
            return data

        # Else we get them.
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_url,
                params={"tags": tag, "limit": 100},
                headers=self.headers,
            ) as response:
                if response.ok:
                    data = await response.json()
                    log.debug("Found %s posts with tag(s) '%s'" % (len(data), tag))
                    for post in data["posts"]:
                        try:
                            post["file"]["url"]
                            post["id"]
                        except Exception as e:
                            log.warning("A post was missing %s!" % str(e))
                            continue
                        if not post["file"]["url"]:
                            continue
                        if not post["file"]["url"].split(".")[-1] in [
                            "mp4",
                            "webm",
                        ]:
                            posts.append(
                                BooruPost(
                                    post["file"]["url"],
                                    self.post_url.format(id=post["id"]),
                                )
                            )
                    await self.cache.add(tag, posts, duration=500)
                    return posts


class Cog(commands.Cog, name="NSFW Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.danbooru = DanbooruClient(bot)
        self.e621 = E621Client(bot)
        self.gelbooru = GelbooruClient(bot)
        self.hypnohub = DanbooruClient(
            bot,
            "https://hypnohub.net/post/index.json",
            "https://hypnohub.net/post/show/{id}",
        )
        self.konachan = DanbooruClient(
            bot,
            "http://konachan.com/post.json",
            "https://konachan.com/post/show/{id}",
        )
        self.realbooru = GelbooruClient(
            bot,
            "https://realbooru.com/index.php",
            "https://realbooru.com",
            True,
        )
        self.rule34 = GelbooruClient(
            bot,
            "https://rule34.xxx/index.php",
            "https://rule34.xxx",
            True,
        )

    @commands.command(
        description="Get a random image from a specified tag from DanBooru. (NSFW)",
        usage="{prefix}danbooru <tags>",
        name="danbooru",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _danbooru(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.danbooru.get_posts(tags)
            embed = construct_post_embed(
                tags, posts, "Note: Danbooru only allows 2 tags in one search."
            )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from e621. (NSFW, Furry site)",
        usage="{prefix}e621 <tags>",
        name="e621",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _e621(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.e621.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from GelBooru. (NSFW)",
        usage="{prefix}gelbooru <tags>",
        name="gelbooru",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _gelbooru(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.gelbooru.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from HypnoHub. (NSFW Hypno fetish site)",
        usage="{prefix}hypnohub <tags>",
        name="hypnohub",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _hypnohub(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.hypnohub.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from KonaChan. (NSFW)",
        usage="{prefix}konachan <tags>",
        name="konachan",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _konachan(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.konachan.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from RealBooru. (NSFW)",
        usage="{prefix}realbooru <tags>",
        name="realbooru",
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _realbooru(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.realbooru.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(
        description="Get a random image from a specified tag from Rule34. (NSFW)",
        usage="{prefix}rule34 <tags>",
        name="rule34",
        aliases=["r34"],
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def _rule34(self, ctx, *, tags=""):
        async with ctx.typing():
            posts = await self.rule34.get_posts(tags)
            embed = construct_post_embed(tags, posts)
        await ctx.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Cog(bot))
