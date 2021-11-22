import discord
import config
import requests

from cmdtools.ext.command import Command, CommandWrapper
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
        
        for command in utility.get_commands():
            cmdobj = utility.load_command(command)
            
            if cmdobj and command in config.PREFIXES:
                embed.add_field(
                    name=f"{command.lower().capitalize().replace('_', ' ')}: {config.PREFIXES[command]}",
                    value=", ".join([cmd.name for cmd in cmdobj.group.commands]),
                    inline=False,
                )

        await self.message.reply(embed=embed)


@group.command()
class HostInfo(Command):
    prefix = config.PREFIXES["general"]
    category = "General"

    def __init__(self):
        super().__init__(name="hostinfo")

    @property
    def help(self):
        return "Get bot host info."
        
    async def hostinfo(self):
        req = requests.get("https://api.ipify.org", params={"format": "json"})
        
        if req.status_code == 200:
            req = requests.get("http://ip-api.com/json/" + req.json()['ip'])
            
            if req.status_code == 200:
                if req.json()['status'] == "success":
                    embed = discord.Embed(title="Host Info", color=0x00FF00)
                    embed.description = f"Country: **{req.json()['country']}**\nCity: **{req.json()['city']}**\nTimezone: **{req.json()['timezone']}**"
                    
                    await self.message.reply(embed=embed)
                else:
                    await self.message.reply("Failed to get host info!")
