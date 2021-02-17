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
        self.bot.last_status_at = None
        self.bot.status = None
        self.bot.midnight = datetime.time(hour=0)
        self.bot.loop.create_task(self.status())
        self.bot.loop.create_task(self.pur())
        self.bot.loop.create_task(self.cleanse_dict())

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
            if len([x[0]['message'] for x in pur.update_requirements(input_file='requirements.txt').values()]) != 0:
                useful_functions.logger.info(str([x[0]['message'] for x in pur.update_requirements(input_file='requirements.txt').values()]))
            await asyncio.sleep(60)

    async def status(self):
        await self.bot.wait_until_ready()
        while True:
            if (datetime.datetime.utcnow()-self.bot.last_status_at).minutes < 5 or self.bot.last_status_at is None:
                async with aiosqlite.connect('storage.db') as db:
                    async with db.execute("SELECT * FROM Statuses ORDER BY RANDOM() LIMIT 1;") as cursor:
                        status = (await cursor.fetchone())[0]
                if status != self.bot.status:
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                             name=f"{status} - {len(self.bot.guilds):,} servers and {len(self.bot.users):,} members!"))
                    useful_functions.logger.info(f"New status: {status}")
                    self.bot.status = status
                self.bot.last_status_at = datetime.datetime.utcnow()
            await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(Tasks(bot))
