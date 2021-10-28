import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

TOKEN = os.getenv("TOKEN", "no token")
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN", "no token")
TENOR_TOKEN = os.getenv("TENOR_TOKEN", "no token")

# reddit config
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "no")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "no")

GUILD = 877498494879952937
PREFIXES = {"music": "b+", "anime": "a+", "general": "b!", "reddit": "r+", "fun": "f+"}

# website config
HOST = os.getenv("BOT_HOST", "120.0.0.1")
PORT = os.getenv("BOT_PORT", 5555)


class Version(Enum):
    PATCH = 0
    MINOR = 2
    MAJOR = 0

    def __str__(self):
        return f"{self.MAJOR.value}.{self.MINOR.value}.{self.PATCH.value}"
