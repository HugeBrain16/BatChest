import random
import requests
import discord
import cmdtools
from cmdtools.ext.command import Command, CommandWrapper


group = CommandWrapper()


@group.command()
class Dice(Command):
    def __init__(self):
        super().__init__(name="dice")
        
    async def dice(self):
        dice = random.randint(1, 6)
        
        await self.message.reply(f"Your dice is **{dice}**")


@group.command()
class Joke(Command):
    def __init__(self):
        super().__init__(name="joke")
        
    async def joke(self):
        retries = 0
        url = "https://icanhazdadjoke.com/"

        joke = requests.get(url, headers={"Accept": "text/plain"})
        
        while joke.status_code != 200 and retries < 3:
            retries += 1
            joke = requests.get(url, headers={"Accept": "text/plain"})

            if joke.status_code == 200:
                await self.message.reply(joke.text)
                break
        else:
            if joke.status_code == 200:
                await self.message.reply(joke.text)
            else:
                await self.message.reply("Error fetching joke!")


@group.command()
class Magic8Ball(Command):
    __aliases__ = ["magic8ball", "m8ball"]

    def __init__(self):
        super().__init__(name="8ball")
        
    @property
    def callback(self):
        return self._8ball
        
    async def error_8ball(self, error):
        if isinstance(error, cmdtools.MissingRequiredArgument):
            if error.param == "question":
                await self.message.reply("You need to ask a question!")
        else:
            raise error

    async def _8ball(self, *question):
        if question:
            _question = " ".join(question)
        else:
            raise cmdtools.MissingRequiredArgument("invoke", "question")
            
        answers = [
            # affirmative
            {"text": "It is certain.", "color": 0x02590f},
            {"text": "It is decidedly so.", "color": 0x02590f},
            {"text": "Without a doubt.", "color": 0x02590f},
            {"text": "Yes definitely.", "color": 0x02590f},
            {"text": "You may rely on it.", "color": 0x02590f},
            {"text": "As I see it, yes.", "color": 0x02590f},
            {"text": "Most likely.", "color": 0x02590f},
            {"text": "Outlook good.", "color": 0x02590f},
            {"text": "Yes.", "color": 0x02590f},
            {"text": "Signs point to yes.", "color": 0x02590f},
                
            # non-committal
            {"text": "Reply hazy, try again.", "color": 0xffff00},
            {"text": "Ask again later.", "color": 0xffff00},
            {"text": "Better not tell you now.", "color": 0xffff00},
            {"text": "Cannot predict now.", "color": 0xffff00},
            {"text": "Concentrate and ask again.", "color": 0xffff00},
            
            # negative
            {"text": "Don't count on it.", "color": 0xff0000},
            {"text": "My reply is no.", "color": 0xff0000},
            {"text": "My sources say no.", "color": 0xff0000},
            {"text": "Outlook not so good.", "color": 0xff0000},
            {"text": "Very doubtful.", "color": 0xff0000},
        ]

        answer = random.choice(answers)
        embed = discord.Embed(title=answer['text'], color=answer['color'])
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Magic8ball.jpg/220px-Magic8ball.jpg")
        embed.set_author(name=_question)
        embed.set_footer(text=f"Asked by {self.message.author.display_name}")

        await self.message.reply(embed=embed)
