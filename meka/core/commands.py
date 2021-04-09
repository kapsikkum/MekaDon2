# @Author: kapsikkum
# @Date:   2021-04-02 07:35:02
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-09 14:02:29


import discord
from discord.ext import commands
from meka.core.utils import construct_extension_embed


class Basic(
    commands.Cog, name="Basic Commands", description="The bot's general basic commands."
):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Pings the bot. That's it, that's all it does.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"**{int(self.bot.latency * 1000)} ms**", mention_author=False)


class Admin(
    commands.Cog, name="Admin Commands", description="Commands for moderation etc."
):
    pass


class Owner(commands.Cog, name="Owner Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        description="Commands for interacting with the bots loaded extensions.",
        aliases=["ext", "exts"],
        hidden=True,
        invoke_without_command=True,
    )
    @commands.is_owner()
    async def extensions(self, ctx):
        await ctx.reply(
            embed=construct_extension_embed(self.bot),
            mention_author=False,
        )

    @extensions.group(
        description="Reload the currently loaded extensions (And any that are found).",
        aliases=["r", "rel"],
        invoke_without_command=True,
    )
    @commands.is_owner()
    async def reload(self, ctx):
        self.bot.reload_extensions()
        await ctx.reply(
            embed=construct_extension_embed(self.bot, text="Reloaded Extensions."),
            mention_author=False,
        )

    @reload.command(
        description="Reload the bot.",
        name="bot",
        aliases=["b"],
    )
    @commands.is_owner()
    async def _bot(self, ctx):
        await ctx.reply("Reloading the bot!", mention_author=False)
        await self.bot.close()
        # and we would restart the bot from the outside!


def setup(bot):
    bot.add_cog(Basic(bot))
    bot.add_cog(Owner(bot))
