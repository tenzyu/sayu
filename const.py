from os import getenv

from dotenv import load_dotenv

load_dotenv()

# get token from .env
DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")

# bot settings
BOT_NAME = str(getenv("BOT_NAME", "Sayu"))
BOT_PREFIX = str(getenv("BOT_PREFIX", "?"))

# channel ids
CHANNEL_ID_TASK_MANAGER = int(getenv("CHANNEL_ID_TASK_MANAGER", "857068721545805844"))
