import aiosqlite
import discord
import datetime
import pur
from utils import useful_functions
from discord.ext import commands, tasks


class Tasks(commands.Cog, description='Some tasks loops to keep the bot up and running.'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.status = ""
        self.bot.midnight = datetime.time(hour=0)
        self.status.start()
        self.pur.start()
        self.bot.loop.create_task(self.cleanse_dict())

    async def cleanse_dict(self):
        while True:
            now = datetime.datetime.utcnow()
            date = now.date()
            if now.time() > self.bot.midnight:
                date = now.date() + datetime.timedelta(days=1)
                self.bot.guild_senders.clear()
            await discord.utils.sleep_until(datetime.datetime.combine(date, self.bot.midnight))

    @tasks.loop(minutes=5)
    async def status(self):
        async with aiosqlite.connect('storage.db') as db:
            async with db.execute("SELECT * FROM Statuses ORDER BY RANDOM() LIMIT 1;") as cursor:
                status = (await cursor.fetchone())[0]
        if status != self.bot.status:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                     name=f"{status} - {len(self.bot.guilds):,} servers and {len(self.bot.users):,} members!"))
            useful_functions.logger.info(f"New status: {status}")
            self.bot.status = status

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1)
    async def pur(self):
        if len([x[0]['message'] for x in pur.update_requirements(input_file='requirements.txt').values()]) != 0:
            useful_functions.logger.info(str([x[0]['message'] for x in pur.update_requirements(input_file='requirements.txt').values()]))


def setup(bot):
    bot.add_cog(Tasks(bot))
