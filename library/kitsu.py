"""Kitsu.io API Wrapper"""

import requests
import random
import datetime
from typing import List
from enum import Enum

BASE = "https://kitsu.io/api/edge"


class ImageSize(Enum):
    ORIGINAL = "original"
    SMALL = "small"
    TINY = "tiny"
    MEDIUM = "medium"
    LARGE = "large"


class ContentType(Enum):
    ANIME = "anime"
    MANGA = "manga"


class MediaDefault(Enum):
    NOT_FOUND = "https://gcdn.pbrd.co/images/zkdbeZmdYByv.gif"


class Anime:
    def __init__(self, anime_id: int):
        self.request = requests.get(BASE + "/anime/" + str(anime_id))
        self.data = self.request.json()["data"]

    def __dict__(self) -> dict:
        return self.data

    @property
    def id(self) -> int:
        return int(self.data["id"])

    @property
    def type(self) -> ContentType:
        return ContentType[self.data["type"]]

    @property
    def episodes(self) -> int:
        return self.data["attributes"].get("episodeCount", 0)

    @property
    def url(self) -> str:
        return "https://kitsu.io/anime/" + str(self.id)

    @property
    def api_url(self) -> str:
        return BASE + "/anime/" + str(self.id)

    @property
    def title(self) -> str:
        return self.data["attributes"]["titles"].get("en", "-")

    @property
    def title_jp(self) -> str:
        return self.data["attributes"]["titles"].get("en_jp", "-")

    @property
    def title_ja(self) -> str:
        return self.data["attributes"]["titles"].get("ja_jp", "-")

    @property
    def description(self) -> str:
        return self.data["attributes"]["description"]

    @property
    def nsfw(self) -> bool:
        return self.data["attributes"]["nsfw"]

    @property
    def synopsis(self) -> str:
        return self.data["attributes"]["synopsis"]

    def get_poster_image(self, size: ImageSize = ImageSize.ORIGINAL) -> str:
        poster = self.data["attributes"]["posterImage"]
        if poster is not None:
            return poster.get(size.value)

        return MediaDefault.NOT_FOUND.value

    def get_cover_image(self, size: ImageSize = ImageSize.ORIGINAL) -> str:
        cover = self.data["attributes"]["coverImage"]
        if cover is not None:
            return cover.get(size.value)

        return MediaDefault.NOT_FOUND.value

    def genre_list(self) -> list:
        req = requests.get(self.api_url + "/genres")

        return [
            data["attributes"]["name"].lower().capitalize()
            for data in req.json()["data"]
        ]

    def discord_embed(self, cover: bool = False):
        import discord

        readmore = f"...\n\n[read more]({self.url})"
        embed = discord.Embed(
            title=self.title_jp[: 256 - len("...")]
            + (
                "..."
                if len(self.title_jp) > (256 - len("..."))
                else self.title_jp[256 - len("...") :]
            ),
            url=self.url,
            color=0x87CEEB if not self.nsfw else 0xFF0000,
        )
        embed.description = self.description[: 4096 - len(readmore)] + (
            readmore
            if len(self.description) > (4096 - len(readmore))
            else self.description[4096 - len(readmore) :]
        )
        embed.set_thumbnail(url=self.get_poster_image(ImageSize.LARGE))
        embed.set_footer(
            text="Kitsu.io"
            + (", Content with embed color Red is NSFW" if self.nsfw else "")
        )
        if cover:
            embed.set_image(url=self.get_cover_image(ImageSize.LARGE))

        # fields
        embed.add_field(name="Total Episodes", value=self.episodes)
        embed.add_field(
            name="Alternative Titles",
            value=f"Japanese: **{self.title_ja}**\nEnglish: **{self.title}**",
        )
        embed.add_field(name="Genres", value=", ".join(self.genre_list()) + ".")
        embed.add_field(name="Rating", value=self.data["attributes"]["averageRating"])
        embed.add_field(
            name="Status", value=self.data["attributes"]["status"].capitalize()
        )
        embed.add_field(
            name="Year",
            value=datetime.datetime.strptime(
                self.data["attributes"]["startDate"], "%Y-%m-%d"
            ).year,
        )

        return embed


def search_anime(query: str, limit: int = 5) -> List[Anime]:
    req = requests.get(BASE + "/anime", params={"filter[text]": query})
    return [Anime(int(data["id"])) for data in req.json()["data"][:limit]]


def random_anime(limit: int = 5) -> List[Anime]:
    req = requests.get(BASE + "/anime")
    result = []

    while len(result) < limit:
        random_id = random.randint(1, req.json()["meta"]["count"])
        areq = requests.get(BASE + "/anime/" + str(random_id))
        if areq.status_code == 200:
            result.append(Anime(random_id))

    return result
