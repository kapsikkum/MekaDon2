# @Author: kapsikkum
# @Date:   2021-04-02 07:35:02
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-02 09:17:36

from discord.ext import commands


class Cog(commands.Cog, name="Internal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Pings the bot. That's it, that's all it does.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"**{int(self.bot.latency * 1000)} ms**")


def setup(bot):
    bot.add_cog(Cog(bot))
