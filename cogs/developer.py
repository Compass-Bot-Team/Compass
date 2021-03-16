# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import asyncio
import aiosqlite
import json
from utils import useful_functions, embeds, exceptions, checks
from discord.ext import commands


class Developer(commands.Cog, description='A bunch of commands for the owner of the bot to use.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.group(invoke_without_command=True, help="Basically eval but shell. Owner only command.")
    async def shell(self, ctx, *, command: str):
        directory = os.getcwd()
        returned = ""
        async with ctx.channel.typing():
            proc = await asyncio.create_subprocess_shell(f"cd {directory} & {command}", stdout=asyncio.subprocess.PIPE,
                                                         stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            if stdout:
                returned += f'\n[stdout]\n{stdout.decode()}'
            if stderr:
                returned += f'\n[stderr]\n{stderr.decode()}'
            if proc.returncode == 0:
                await ctx.message.add_reaction('\U0001f7e9')
            else:
                await ctx.message.add_reaction('\U0001f7e5')
        await ctx.send(f'```py\nReturned code {proc.returncode}\n{returned}\n```')

    @shell.command(help="Runs SQL code.", aliases=["SQL"])
    async def sql(self, ctx, *, command: str):
        async with aiosqlite.connect("storage.db") as db:
            if command.startswith("SELECT "):
                execute = await db.execute(command)
            else:
                execute = await db.execute(command)
                await db.commit()
            result = await execute.fetchall()
        await ctx.send(result)

    @sql.error
    async def sql_error(self, ctx, error):
        await ctx.message.add_reaction("<:compass_bot_no:809974728915419177>")
        return await ctx.send(error)

    @commands.is_owner()
    @commands.command(help='Reloads a cog. Use the cog list command to get the full list of cogs.')
    async def reload(self, ctx, *, extension: str):
        alls = ["all", "All"]
        if extension in alls:
            for cog in self.bot.cogs_tuple:
                self.bot.reload_extension(cog)
                useful_functions.logger.info(f"Loaded cog {cog}")
            return await ctx.send(embed=embeds.twoembed(f"Success!",
                                                        f"Reloaded every cog."))
        elif ", " in extension:
            extensions = extension.split(", ")
            for cog in extensions:
                self.bot.reload_extension(str("cogs." + cog))
                useful_functions.logger.info(f"Reloaded cog {cog}")
            return await ctx.send(embed=embeds.twoembed(f"Success!",
                                                        f"Reloaded cogs.{extension}."))
        else:
            self.bot.reload_extension(str("cogs." + extension))
            useful_functions.logger.info(f"Reloaded cog cogs.{extension}")
            await ctx.send(embed=embeds.twoembed(f"Success!",
                                                 f"Reloaded cogs.{extension}."))

    @commands.is_owner()
    @commands.command(help="Closes the bot connection. Owner command.", aliases=["stop"])
    async def shutdown(self, ctx):
        channel = self.bot.get_channel(801974572244140033)
        embed = embeds.failembed("Shutting down...", f"Bot shutdown ordered by {ctx.author}.")
        await ctx.send(embed=embed)
        await channel.send(embed=embed)
        await self.bot.close()
        # fall back
        loop = asyncio.get_event_loop()
        loop.stop()

    @commands.is_owner()
    @commands.group(invoke_without_command=True, help="Manage command for the bot blacklist.")
    async def blacklist(self, ctx):
        raise exceptions.MissingSubcommand("No subcommand found!")

    async def check_if_in_blacklist(self, target):
        blacklist_file = (self.get_blacklist())["blacklist"]
        if target[1] == "guild" and target[2].id in blacklist_file["guilds"]:
            return False
        elif target[1] == "user" and target[2].id in blacklist_file["users"]:
            return False
        else:
            [blacklist_file[str(target[1])+"s"]].append(target[2].id)
        #with open("mainbank.json", "w") as f:
        #    json.dump(users, f)
        return True

    @staticmethod
    def get_blacklist():
        with open("blacklist.json") as file:
            blacklist = json.load(file)
        return blacklist

    @commands.is_owner()
    @blacklist.command(help="Adds a user, or guild ID to the blacklist.")
    async def add(self, ctx, *, target: checks.UserOrGuild):
        pass
#        if target[1] == "guild":



def setup(bot):
    bot.add_cog(Developer(bot))
