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
from utils import embeds
from utils.useful_functions import prefix
from discord.ext import commands
from utils import useful_functions

logging.basicConfig(**{"format": f"[%(asctime)s %(name)s %(levelname)s] %(message)s", "level": logging.INFO})
logging.Formatter.converter = time.gmtime
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
__VERSION__ = 4.5


class CompassHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        returned = command.qualified_name
        if command.aliases:
            for alias in command.aliases:
                returned += f"/{alias}"
        return returned

    async def send_command_help(self, command):
        channel = self.get_destination()
        async with channel.typing():
            title = self.get_command_signature(command)
            if command.signature:
                title += f" {command.signature}"
            embed = embeds.twoembed(f"``{title}``", command.help)
            embed.url = await source(command.qualified_name)
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        channel = self.get_destination()
        async with channel.typing():
            title = self.get_command_signature(group)
            if group.signature:
                title += f" {group.signature}"
            embed = embeds.twoembed(f"``{title}``", group.short_doc)
            embed.url = await source(group.qualified_name)
            subcommand_count = 0
            subcommands = ""
            if group.commands:
                for subcommand in group.commands:
                    if subcommand_count != 0: subcommands += ", "
                    subcommands += f"``{subcommand}``"
                    subcommand_count += 1
                embed.add_field(name="Subcommands", value=subcommands)
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        channel = self.get_destination()
        embed = embeds.twoembed(f"``{cog.qualified_name}``", cog.description)
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        embed = embeds.twoembed(f"Compass help!", f"The used prefix was {self.clean_prefix}.")
        async with channel.typing():
            for cog, commands in mapping.items():
                filtered = await self.filter_commands(commands, sort=True)
                command_signatures = [self.get_command_signature(c) for c in filtered]
                command_count = 0
                commands_registered = ""
                if command_signatures:
                    for command in command_signatures:
                        if command_count == 0:
                            commands_registered += f"``{command}``"
                        else:
                            commands_registered += f", ``{command}``"
                        command_count += 1
                    cog_name = getattr(cog, "qualified_name", "Other")
                    embed.add_field(name=cog_name, value=commands_registered, inline=False)
        await channel.send(embed=embed)


class Compass(commands.Bot):
    def __init__(self):
        # Constructor
        parameters = {"command_prefix": prefix,
                      "intents": discord.Intents.all(),
                      "description": "Compass is an all-in-one bot coded in discord.py.",
                      "help_command": CompassHelp(command_attrs={'help': "Posts this message."})}
        super().__init__(**parameters)

        self.config = yaml.safe_load(open("config.yml"))
        self.config["github_ids"] = {}
        # Discord ID | GitHub ID
        for owner in self.config["owners"]:
            self.config["github_ids"][38298732] = owner
        self.owner_ids = self.config["owners"]
        self.base_color = 0x202225
        self.directory = os.getcwd()
        self.version = __VERSION__

        # Cache
        self.not_allocated = True
        self.launch_time = datetime.datetime.utcnow()
        self.message_num = 0
        self.command_num = 0
        self.message_senders = {}
        self.guild_senders = {}
        self.command_users = {}
        self.command_guilds = {}

        self.cogs_tuple = ("cogs.antolib", "cogs.apis", "cogs.developer", "cogs.error_handling", "cogs.fun",
                           "cogs.images", "cogs.moderation", "cogs.music", "cogs.tasks", "cogs.utilities",
                           "cogs.websocket")

        # Loads cogs
        for cog in self.cogs_tuple:
            self.load_extension(cog)
            useful_functions.logger.info(f"Loaded cog {cog}")

        self.load_extension("jishaku")
        useful_functions.logger.info(f"Loaded cog jishaku (outside of main folder)")

    def run(self):
        super().run(self.config["token"])


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
