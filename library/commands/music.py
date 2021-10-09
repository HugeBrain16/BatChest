import discord
import cmdtools
import config

from cmdtools.ext.command import CommandWrapper, Command
from youtubesearchpython import VideosSearch

group = CommandWrapper()

__all__ = [
    "group",
]


@group.command()
class Now(Command):
    _aliases = ["nowplaying", "playing", "now_playing"]
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="now")

    @property
    def help(self):
        return "Show what is the bot playing currently?"

    async def now(self):
        voice = self.client.get_voice()

        if voice:
            if self.client.music.now_playing:
                return await self.message.reply(
                    f"Now playing", embed=self.client.music.now_playing.embed()
                )

        await self.message.reply("Not playing anything currently...")


@group.command()
class Stop(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="stop")

    @property
    def help(self):
        return "Stop and clear queue"

    async def stop(self):
        await self.client.music.clear_queue()
        voice = self.client.get_voice()

        if voice:
            if voice.is_playing():
                await self.message.add_reaction("🛑")
                voice.stop()


@group.command()
class Pause(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="pause")

    @property
    def help(self):
        return "Pause audio"

    async def pause(self):
        voice = self.client.get_voice()

        if voice:
            if voice.is_playing():
                await self.message.add_reaction("⏸")
                voice.pause()


@group.command()
class Skip(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="skip")

    async def skip(self):
        voice = self.client.get_voice()

        if voice:
            if voice.is_playing():
                voice.stop()
                await self.message.add_reaction("⏯")


@group.command(
    help="Resume paused audio", prefix=config.PREFIXES["music"], category="Music"
)
class Resume(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="resume")

    async def resume(self):
        voice = self.client.get_voice()

        if voice:
            if voice.is_paused():
                await self.message.add_reaction("▶")
                voice.resume()


@group.command(
    help="Leave voice channel", prefix=config.PREFIXES["music"], category="Music"
)
class Leave(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="leave")

    async def leave(self):
        if self.client.is_user_in_vc(self.message.author):
            if self.client.is_in_vc():
                if self.client.check_user_vc(self.message.author):
                    await self.client.get_voice().disconnect()
                else:
                    await self.message.reply("You are in a different voice channel")
            else:
                await self.message.reply("I am not connected to a voice channel")
        else:
            await self.message.reply("You are not in a voice channel")


@group.command()
class Join(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="join")

    @property
    def help(self):
        return "Join voice channel"

    async def join(self):
        if self.client.is_user_in_vc(self.message.author):
            if self.client.is_in_vc() is False:
                await self.message.add_reaction("✅")
                await self.message.author.voice.channel.connect()
            else:
                await self.message.reply(f"I am connected to a voice channel")
        else:
            await self.message.reply(f"You are not in a voice channel")


@group.command()
class Play(Command):
    _aliases = [
        "queue",
    ]
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="play")

    @property
    def help(self):
        return "Add a song to queue"

    async def play(self, *query_):
        if query_:
            query = " ".join(query_)
        else:
            raise cmdtools.MissingRequiredArgument("invoke", "query_")

        if self.client.is_user_in_vc(self.message.author):
            if self.client.is_in_vc():
                if self.client.check_user_vc(self.message.author):
                    video = VideosSearch(query, region="SE", limit=1)
                    result = video.result()["result"]
                    if result:
                        await self.client.music.add_song(
                            result[0], message=self.message
                        )
                    else:
                        await self.message.reply(
                            f"Can't find media with search query '{query}'"
                        )
                else:
                    await self.message.reply("You are in a different voice channel")
            else:
                await self.message.reply("I am not connected to a voice channel")
        else:
            await self.message.reply("You are not in a voice channel")

    async def error_play(self, error):
        if isinstance(error, cmdtools.MissingRequiredArgument):
            if error.param == "query_":
                await self.message.reply("You need to provide a search query!")
        else:
            raise error


@group.command()
class Lyrics(Command):
    prefix = config.PREFIXES["music"]
    category = "Music"

    def __init__(self):
        super().__init__(name="lyrics")

    @property
    def help(self):
        return "Get lyrics of a song"

    async def lyrics(self, *query_):
        if query_:
            query = " ".join(query_)
        else:
            raise cmdtools.MissingRequiredArgument("invoke", "query_")

        song = self.client.genius.search_song(query)
        if song:
            embed = discord.Embed(
                title=song.title[:256] + ("..." if len(song.title) > 256 else ""),
                color=0xFFFF00,
            )
            embed.description = song.lyrics[:4096] + (
                "..." if len(song.lyrics) > 4096 else ""
            )
            embed.set_footer(text="Lyrics by Genius")
            embed.set_thumbnail(url=song.song_art_image_thumbnail_url)
            embed.set_author(name="Lyrics")
            embed.url = song.url

            await self.message.reply(embed=embed)
        else:
            await self.message.reply(f"Couldn't find song with query '{query}'")

    async def error_lyrics(self, error):
        if isinstance(error, cmdtools.MissingRequiredArgument):
            if error.param == "query_":
                await self.message.reply("You need to provide a search query!")
        else:
            raise error
