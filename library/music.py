"""music library for the bot"""

import asyncio
from dataclasses import dataclass, field
from typing import Optional

import discord
import youtube_dl


OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}
FFMPEG_OPTS = {
    "before_options": "-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}
YTDL = youtube_dl.YoutubeDL(OPTS)


@dataclass
class Song:
    """dataclass for song request"""
    title: str
    artist: str
    url: str
    message: discord.Message = field(init=False)

    def get_stream_url(self) -> Optional[str]:
        """get youtube stream url"""
        data = YTDL.extract_info(self.url, download=False)

        return data["url"]

    def embed(self) -> discord.Embed:
        """create discord embed"""
        embed = discord.Embed(title=self.title, url=self.url, color=0xFF0000)
        embed.set_author(name=self.artist)

        return embed


class Music:
    """class for music stuff"""
    def __init__(self, client: discord.Client, queue_limit: int = 100):
        self.queue = asyncio.Queue(queue_limit)
        self.client = client

        # properties
        self.now_playing = None

    async def clear_queue(self) -> None:
        """clear all items queue"""
        for _ in range(self.queue.qsize()):
            try:
                self.queue.task_done()
            except ValueError:
                print("Overwhelmed for clearing queue LUL")
        await self.queue.join()

    async def add_song(self, video: dict, message: discord.Message) -> None:
        """add song to queue"""
        song = Song(video["title"], video["channel"]["name"], video["link"])
        song.message = message

        await self.queue.put(song)
        await message.reply("Added on queue!", embed=song.embed())

    def finished_playing(self):
        """called when a song has finished playing"""
        self.queue.task_done()
        self.now_playing = None

    async def play_song(self):
        """play queued song"""
        voice = self.client.get_voice()
        if voice is None:
            return

        if not voice.is_playing():
            self.now_playing = await self.queue.get()
            audio = discord.FFmpegPCMAudio(
                self.now_playing.get_stream_url(), **FFMPEG_OPTS
            )
            await self.now_playing.message.reply(
                "Now playing", embed=self.now_playing.embed()
            )
            voice.play(audio, after=self.finished_playing())

    async def run(self):
        """run instance"""
        while True:
            await self.play_song()
            await asyncio.sleep(1)
