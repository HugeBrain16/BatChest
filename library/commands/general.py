import discord
import config

from cmdtools.ext.command import Command, CommandWrapper
from library.commands import anime
from library.commands import music
from library.commands import reddit
from library import utility

group = CommandWrapper()


@group.command()
class Ping(Command):
    prefix = config.PREFIXES["general"]
    category = "General"

    def __init__(self):
        super().__init__(name="ping")

    @property
    def help(self):
        return "get latency"

    async def ping(self):
        await self.message.reply(f"Pong! (**{self.client.latency * 1000:.2f}ms**)")


@group.command()
class Avatar(Command):
    prefix = config.PREFIXES["general"]
    category = "General"

    def __init__(self):
        super().__init__(name="avatar")

    @property
    def help(self):
        return "Show user's avatar"

    async def avatar(self, mention=None):
        if mention:
            guild = self.client.get_guild(config.GUILD)
            
            user = None
            if guild:
                user = guild.get_member(utility.mention_to_id(mention))

            if user:
                embed = discord.Embed(
                    title=f"{user.display_name}'s Avatar", color=0xFFFFFF
                )
                embed.set_image(url=user.avatar_url)

                await self.message.reply(embed=embed)
            else:
                await self.message.reply("User not found!")
        else:
            embed = discord.Embed(
                title=f"{self.message.author.display_name}'s Avatar", color=0xFFFFFF
            )
            embed.set_image(url=self.message.author.avatar_url)

            await self.message.reply(embed=embed)

    async def error_avatar(self, error):
        raise error


@group.command()
class Help(Command):
    prefix = config.PREFIXES["general"]
    category = "General"

    def __init__(self):
        super().__init__(name="help")

    @property
    def callback(self):
        return self._help

    @property
    def help(self):
        return "Show this"

    async def _help(self):
        embed = discord.Embed(title="Help", color=0xFFFFFF)
        embed.description = (
            "Showing all available commands <a:batPls:896152163582111784>"
        )

        embed.add_field(
            name=f"General: {config.PREFIXES['general']}",
            value=", ".join([cmd.name for cmd in group.commands]),
            inline=False,
        )
        embed.add_field(
            name=f"Music: {config.PREFIXES['music']}",
            value=", ".join([cmd.name for cmd in music.group.commands]),
            inline=False,
        )
        embed.add_field(
            name=f"Anime: {config.PREFIXES['anime']}",
            value=", ".join([cmd.name for cmd in anime.group.commands]),
            inline=False,
        )
        embed.add_field(
            name=f"Reddit: {config.PREFIXES['reddit']}",
            value=", ".join([cmd.name for cmd in reddit.group.commands]),
            inline=False,
        )

        await self.message.reply(embed=embed)
