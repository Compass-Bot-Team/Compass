import asyncio
from discord.ext import commands


class Experimental(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Experimental(bot))
