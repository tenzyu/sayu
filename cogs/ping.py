from time import monotonic

from discord.ext.commands import Bot, Cog, Context, command


class Ping(Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context) -> None:
        """check the connection and response time"""
        tmp = monotonic()
        msg = await ctx.send("Calculating...")
        latency = (monotonic() - tmp) * 1000
        await msg.edit(content=f"Pong! Response time is **{int(latency)}** ms.")


def setup(bot: Bot):
    bot.add_cog(Ping(bot))
