# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import discord
import logging
import yaml
import os
import time
import asyncio
import inspect
import json
from utils.useful_functions import prefix
from discord.ext import commands
from collections import Counter
from utils import useful_functions
from utils.embeds import failembed

logging.basicConfig(**{"format": f"[%(asctime)s %(name)s %(levelname)s] %(message)s", "level": logging.INFO})
logging.Formatter.converter = time.gmtime
# Jishaku environments
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
__VERSION__ = 4.6


class Compass(commands.Bot):
    def __init__(self):
        # Constructor
        constructor = {"command_prefix": prefix,
                       "intents": discord.Intents.all(),
                       "description": "Compass is an all-in-one bot coded in discord.py."}
        super().__init__(**constructor)

        ### Initialize config
        self.config = yaml.safe_load(open("config.yml"))
        self.config["github_ids"] = {}
        # Discord ID | GitHub ID
        # just for later
        for owner in self.config["owners"]:
            self.config["github_ids"][38298732] = owner
        # more config stuff
        self.owner_ids = self.config["owners"]
        self.dtog = self.get_user(721029142602056328)
        self.base_color = 0x202225
        self.directory = os.getcwd()
        self.config["version"] = __VERSION__
        ### Spam control
        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)
        self._auto_spam_count = Counter()

        ### Initialize Cache
        # sqlite only does one at a time
        self.not_allocated = True
        # Launch time for uptime
        self.launch_time = datetime.datetime.utcnow()
        # stats
        self.message_num = 0
        self.command_num = 0
        self.message_senders = {}
        self.guild_senders = {}
        self.command_users = {}
        self.command_guilds = {}

        # non config but oh well
        # If you want to add a cog put in "cogs.cog name"
        self.cogs_tuple = ("cogs.antolib", "cogs.apis", "cogs.developer", "cogs.error_handling", "cogs.fun",
                           "cogs.help", "cogs.images", "cogs.moderation", "cogs.music", "cogs.tasks", "cogs.utilities",
                           "jishaku")

        # Loads cogs
        for cog in self.cogs_tuple:
            self.load_extension(cog)
            if cog == "jishaku":
                cog += " (outside of main folder)"
            useful_functions.logger.info(f"Loaded cog {cog}")

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        with open("blacklist.json") as file:
            blacklist_file = json.load(file)
        blacklist = blacklist_file["blacklist"]
        humans = blacklist["humans"]
        guilds = blacklist["guilds"]
        if ctx.author.id in humans:
            return
        if ctx.guild is not None and ctx.guild.id in guilds:
            return
        await self.invoke(ctx)

    ### Run function
    def run(self):
        super().run(self.config["token"])


### Source function for help command and source command, modified from R. Danny
async def source(command):
    url = "https://github.com/Compass-Bot-Team/Compass/blob/rewrite"
    if command == 'help':
        src = type(Compass().help_command)
        module = src.__module__
        filename = inspect.getsourcefile(src)
    else:
        obj = Compass().get_command(command.replace('.', ' '))
        src = obj.callback.__code__
        module = obj.callback.__module__
        filename = src.co_filename
    lines, firstlineno = inspect.getsourcelines(src)
    if not module.startswith('discord'):
        location = os.path.relpath(filename).replace('\\', '/')
    else:
        location = module.replace('.', '/') + '.py'
    return f'{url}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'


asyncio.run(Compass().run())
