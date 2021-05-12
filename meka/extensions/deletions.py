# @Author: kapsikkum
# @Date:   2021-04-20 08:53:13
# @Last Modified by:   kapsikkum
# @Last Modified time: 2021-05-12 13:52:43

import os

import discord
from discord.ext import commands
from meka.core.models import ExpireList


class Cog(
    commands.Cog,
    name="Deletion Commands",
    description="Commands for deleted messages, etc etc",
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
            await ctx.reply("Nothing deleted.", mention_author=False)


def setup(bot):
    bot.add_cog(Cog(bot))