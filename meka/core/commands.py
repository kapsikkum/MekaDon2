# @Author: kapsikkum
# @Date:   2021-04-02 07:35:02
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-04-12 13:41:44


import os

import discord
from discord.ext import commands
from meka.core.models import ExpireList
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
    def __init__(self, bot):
        self.bot = bot
        self.deletions = dict()
        self.no_delete_channels = dict()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self.deletions.get(str(message.channel.id)):
            self.deletions[str(message.channel.id)] = ExpireList()
        self.deletions[str(message.channel.id)].append(message)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, event):
        for message in event.cached_messages:
            if not self.deletions.get(str(message.channel.id)):
                self.deletions[str(message.channel.id)] = ExpireList()
            self.deletions[str(message.channel.id)].append(message)

    @commands.command(
        description="Make the last deleted message in the channel not deleted anymore."
    )
    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def undelete(self, ctx, amount: int = 1):
        if (
            self.deletions.get(str(ctx.message.channel.id))
            and self.deletions.get(str(ctx.message.channel.id), 0) > 0
        ):
            messages = list(reversed(self.deletions[str(ctx.message.channel.id)]))
            for x in range(0, amount):
                try:
                    message = messages[x]
                except Exception as e:
                    continue
                if len(message.content) != 0:
                    embed = discord.Embed(
                        title=discord.Embed.Empty,
                        description=message.content,
                        color=0xFF0000,
                        timestamp=message.created_at,
                    )
                    embed.set_footer(
                        text=message.author.name, icon_url=message.author.avatar_url
                    )
                    await ctx.send(embed=embed)

                for embed in message.embeds:
                    embed.set_footer(
                        text=message.author.name, icon_url=message.author.avatar_url
                    )
                    await ctx.send(embed=embed)

                for attachment in message.attachments:
                    filetype = os.path.splitext(attachment.url)[1]
                    if filetype in [".png", ".webp", ".jpg", ".jpeg", ".gif"]:
                        embed = discord.Embed(
                            title="Deleted Image",
                            description=discord.Embed.Empty,
                            color=0xFF0000,
                            timestamp=message.created_at,
                        )
                        embed.set_image(
                            url=attachment.url.replace(
                                "cdn.discordapp.com", "media.discordapp.net"
                            )
                        )
                        embed.set_footer(
                            text=message.author.name,
                            icon_url=message.author.avatar_url,
                        )
                        await ctx.send(embed=embed)

                    elif filetype in [".webm", ".mp4", ".mov"]:
                        embed = discord.Embed(
                            title="Deleted Video",
                            description=discord.Embed.Empty,
                            color=0xFF0000,
                            timestamp=message.created_at,
                        )
                        embed.set_footer(
                            text=message.author.name,
                            icon_url=message.author.avatar_url,
                        )
                        await ctx.send(
                            attachment.url.replace(
                                "cdn.discordapp.com", "media.discordapp.net"
                            ),
                            embed=embed,
                        )

                    else:
                        await ctx.send(
                            attachment.url.replace(
                                "cdn.discordapp.com", "media.discordapp.net"
                            ),
                        )

                try:
                    self.deletions[str(ctx.message.channel.id)].remove(message)
                except Exception as e:
                    pass
        else:
            await ctx.reply("Nothing deleted.")
        # if not str(ctx.message.channel.id) in core.deletions:
        #     raise core.exceptions.CommandError("Nothing was deleted here.")
        # elif len(core.deletions[str(ctx.message.channel.id)]) == 0:
        #     raise core.exceptions.CommandError("Nothing was deleted here.")
        # else:
        #     messages = list(reversed(core.deletions[str(ctx.message.channel.id)]))
        #     for x in range(0, amount):
        #         try:
        #             message = messages[x]
        #         except:
        #             pass
        #         else:


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
    bot.add_cog(Admin(bot))
    bot.add_cog(Owner(bot))
