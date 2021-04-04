# @Author: kapsikkum
# @Date:   2021-04-02 07:35:02
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-03 06:59:50

import discord
from discord.ext import commands


class Basic(
    commands.Cog, name="Basic Commands", description="The bot's general basic commands."
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Pings the bot. That's it, that's all it does.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"**{int(self.bot.latency * 1000)} ms**", mention_author=False)

    @commands.command(description="Shows Currently Loaded Extensions.", hidden=True)
    @commands.is_owner()
    async def extensions(self, ctx):
        ext = "```\n"
        for e in self.bot.loaded_extensions:
            ext += e + "\n"
        ext += "\n```"
        await ctx.reply(
            embed=discord.Embed(
                title="Currently Loaded Extensions",
                description=ext,
                color=0xFF0000,
            ),
            mention_author=False,
        )

    @commands.command(description="Reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx):
        self.bot.reload_extensions()

        ext = "```\n"
        for e in self.bot.loaded_extensions:
            ext += e + "\n"
        ext += "\n```"
        await ctx.reply(
            embed=discord.Embed(
                title="Currently Loaded Extensions",
                description=ext,
                color=0xFF0000,
            ),
            mention_author=False,
        )


def setup(bot):
    bot.add_cog(Basic(bot))
