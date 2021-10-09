import discord
import random
import config
import asyncprawcore

from cmdtools.ext.command import Command, CommandWrapper

group = CommandWrapper()


@group.command()
class Meme(Command):
    prefix = config.PREFIXES["reddit"]
    category = "Reddit"

    def __init__(self):
        super().__init__(name="meme")
        
    @property
    def help(self):
        return "Terrible reddit memes"

    async def meme(self):
        subreddit = await self.client.reddit.subreddit("memes", fetch=True)
        result = []
        
        async for submission in subreddit.hot(limit=128):
            if submission.url:
                result.append(submission)
            
        submission = random.choice(result)
        embed = discord.Embed(color=0xFFFF00)
        if submission.title:
            embed.title = submission.title
        embed.set_image(url=submission.url)

        await self.message.reply(embed=embed)

    async def error_meme(self, error):
        if isinstance(error, asyncprawcore.RequestException):
            await self.message.reply("Couldn't fetch media, try again.")
        else:
            raise error
