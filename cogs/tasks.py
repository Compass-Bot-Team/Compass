# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import aiosqlite
import discord
import datetime
import asyncio
import pur
from utils import useful_functions
from discord.ext import commands, tasks


class Tasks(commands.Cog, description='Some tasks loops to keep the bot up and running.'):
    def __init__(self, bot):
        self.bot = bot
        self.bot.midnight = datetime.time(hour=0)

    async def cleanse_dict(self):
        await self.bot.wait_until_ready()
        while True:
            now = datetime.datetime.utcnow()
            date = now.date()
            if now.time() > self.bot.midnight:
                date = now.date() + datetime.timedelta(days=1)
                self.bot.guild_senders.clear()
            await discord.utils.sleep_until(datetime.datetime.combine(date, self.bot.midnight))

    async def pur(self):
        while True:
            changes_to_requirements = [x[0]['message'] for x in pur.update_requirements(input_file='requirements.txt').values()]
            if len(changes_to_requirements) != 0:
                useful_functions.logger.info(str(changes_to_requirements))
            await asyncio.sleep(60)

    @tasks.loop(minutes=5)
    async def status(self):
        async with aiosqlite.connect('storage.db') as db:
            async with db.execute("SELECT * FROM Statuses ORDER BY RANDOM() LIMIT 1;") as cursor:
                status = (await cursor.fetchone())[0]
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                 name=status))
        useful_functions.logger.info(f"New status: {status}")

    @commands.Cog.listener()
    async def on_ready(self):
        self.status.start()
        self.bot.loop.create_task(self.cleanse_dict())
        self.bot.loop.create_task(self.pur())


def setup(bot):
    bot.add_cog(Tasks(bot))
