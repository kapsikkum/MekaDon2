# @Author: kapsikkum
# @Date:   2021-04-02 07:35:02
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 13:39:25

from discord.ext import commands


class Cog(commands.Cog, name="Internal", description="The bot's base commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Pings the bot. That's it, that's all it does.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"**{int(self.bot.latency * 1000)} ms**", mention_author=False)


def setup(bot):
    bot.add_cog(Cog(bot))
