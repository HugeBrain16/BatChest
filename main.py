"""main bot script"""

import discord
import discord.utils
import cmdtools
import lyricsgenius
import asyncpraw

import web
import config

from library.music import Music
from library.commands import music
from library.commands import anime
from library.commands import general
from library.commands import reddit
from library.commands import fun


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

        cmd_music = cmdtools.AioCmd(message.content, prefix=config.PREFIXES["music"])
        cmd_anime = cmdtools.AioCmd(message.content, prefix=config.PREFIXES["anime"])
        cmd_general = cmdtools.AioCmd(
            message.content, prefix=config.PREFIXES["general"]
        )
        cmd_reddit = cmdtools.AioCmd(message.content, prefix=config.PREFIXES["reddit"])
        cmd_fun = cmdtools.AioCmd(message.content, prefix=config.PREFIXES["fun"])

        if message.guild.id == config.GUILD:
            if cmd_music.name:
                await music.group.run(
                    cmd_music, attrs={"message": message, "client": self}
                )
            elif cmd_anime.name:
                await anime.group.run(
                    cmd_anime, attrs={"message": message, "client": self}
                )
            elif cmd_general.name:
                await general.group.run(
                    cmd_general, attrs={"message": message, "client": self}
                )
            elif cmd_reddit.name:
                await reddit.group.run(
                    cmd_reddit, attrs={"message": message, "client": self}
                )
            elif cmd_fun.name:
                await fun.group.run(
                    cmd_reddit, attrs={"message": message, "client": self}
                )


if __name__ == "__main__":
    print(f"Starting BatChest v{config.Version(0)} ...")
    bot = Bot()
    web.server.start()
    bot.run(config.TOKEN)
