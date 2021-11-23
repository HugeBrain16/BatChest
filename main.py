"""main bot script"""

import discord
import discord.utils
import cmdtools
import lyricsgenius
import asyncpraw
import datetime

import web
import config

from library import utility
from library.music import Music


class Bot(discord.Client):
    """BatChest bot instance"""

    def __init__(self):
        self.genius = lyricsgenius.Genius(config.GENIUS_TOKEN)
        self.reddit = asyncpraw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent="Reddit?! Haha Wowzers!!11! BatChest",
        )
        self.music = Music(self)

        super().__init__()

    def get_voice(self) -> discord.VoiceClient:
        """get bot voice client"""
        return discord.utils.get(self.voice_clients, guild=self.get_guild(config.GUILD))

    @classmethod
    def is_user_in_vc(cls, member: discord.Member) -> bool:
        """check if user is in any voice channel"""
        return not member.voice

    def is_in_vc(self) -> bool:
        """check if client is in any voice channel"""
        return not self.get_voice()

    def check_user_vc(self, user: discord.Member) -> bool:
        """check if user is in same voice channel as the client"""
        return (self.get_voice().channel.id if self.get_voice() is not None else 0) == (
            user.voice.channel.id if user.voice is not None else 1
        )

    async def on_ready(self):
        """called when bot client is ready"""
        self.start_time = datetime.datetime.utcnow()
        voice = self.get_voice()

        if voice:
            await voice.disconnect()

        self.loop.create_task(self.music.run())

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{config.PREFIXES['general']}help",
            )
        )

        print("I'm Ready BatChest")

    async def on_disconnect(self):
        """called when client disconnected"""
        voice = self.get_voice()

        if voice:
            await voice.disconnect()

    async def on_message(self, message):
        """called when new guild message created"""
        if message.author.bot or isinstance(message.channel, discord.channel.DMChannel):
            return

        if message.guild.id == config.GUILD:
            for command in utility.get_commands():
                cmdobj = utility.load_command(command)
                
                if cmdobj and command in config.PREFIXES:
                    cmd = cmdtools.AioCmd(message.content, prefix=config.PREFIXES[command])

                    if cmd.name:
                        await cmdobj.group.run(
                            cmd, attrs={"message": message, "client": self}
                        )


if __name__ == "__main__":
    print(f"Starting BatChest v{config.Version(0)} ...")
    bot = Bot()
    web.server.start()
    bot.run(config.TOKEN)
