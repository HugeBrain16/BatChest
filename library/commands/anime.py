import random
import config
from cmdtools.ext.command import CommandWrapper, Command
from library import kitsu
from library import tenor

group = CommandWrapper()


@group.command()
class Anime(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="anime")

    @property
    def help(self):
        return "Search for anime"

    async def anime(self, *query_):
        query = ""
        if query_:
            query = " ".join(query_)
            anime = kitsu.search_anime(query, limit=1)
        else:
            anime = kitsu.random_anime(limit=1)

        if anime:
            await self.message.reply(embed=anime[0].discord_embed(cover=True))
        else:
            await self.message.reply(f"Not found: '{query}'")

    async def error_anime(self, error: Exception):
        raise error


@group.command()
class Cute(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="cute")

    async def cute(self):
        gifs = tenor.search_gif("anime cute", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_cute(self, error: Exception):
        raise error


@group.command()
class Gif(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="gif")

    @property
    def help(self):
        return "Random anime gif"

    async def gif(self):
        gifs = tenor.search_gif("anime", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_gif(self, error: Exception):
        raise error


@group.command()
class Blush(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="blush")

    async def blush(self):
        gifs = tenor.search_gif("anime blush", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_blush(self, error: Exception):
        raise error


@group.command()
class Smug(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="smug")

    async def smug(self):
        gifs = tenor.search_gif("anime smug", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_smug(self, error: Exception):
        raise error


@group.command()
class Hug(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="hug")

    async def hug(self):
        gifs = tenor.search_gif("anime hug", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_hug(self, error: Exception):
        raise error


@group.command()
class Angry(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="angry")

    async def angry(self):
        gifs = tenor.search_gif("anime angry", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_angry(self, error: Exception):
        raise error


@group.command()
class Lol(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="lol")

    async def lol(self):
        gifs = tenor.search_gif("anime laugh", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_lol(self, error: Exception):
        raise error


@group.command()
class Cry(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="cry")

    async def cry(self):
        gifs = tenor.search_gif("anime cry", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_cry(self, error: Exception):
        raise error


@group.command()
class Eat(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="eat")

    async def eat(self):
        gifs = tenor.search_gif("anime eat", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_eat(self, error: Exception):
        raise error


@group.command()
class Pat(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="pat")

    async def pat(self):
        gifs = tenor.search_gif("anime pat", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_pat(self, error: Exception):
        raise error


@group.command()
class Think(Command):
    prefix = config.PREFIXES["anime"]
    category = "Anime"

    def __init__(self):
        super().__init__(name="think")

    async def think(self):
        gifs = tenor.search_gif("anime think", config.TENOR_TOKEN, limit=128)
        await self.message.reply(
            gifs["results"][random.randint(0, len(gifs["results"]))]["media"][0]["gif"][
                "url"
            ]
        )

    async def error_think(self, error: Exception):
        raise error
