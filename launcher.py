from pathlib import Path
from traceback import print_exc

from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or

import const


class MyBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or(const.BOT_PREFIX),
            intents=Intents.all()
        )
        print(f"Launching {const.BOT_NAME}")

        for cog in Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"Loaded Extension: {cog.stem}")
            except Exception:
                print_exc()

    async def on_ready(self):
        print(f"Logged in as: {self.user.name} {self.user.id}")


if __name__ == "__main__":
    bot = MyBot()
    bot.run(const.DISCORD_BOT_TOKEN)
