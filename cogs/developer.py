# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import asyncio
import aiosqlite
import json
import pygit2
import itertools
import discord
from utils import useful_functions, embeds
from utils.useful_functions import format_commit
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

    async def target_getter(self, target):
        user = self.bot.get_user(target)
        if user is None:
            guild = self.bot.get_guild(target)
            if guild is None:
                raise commands.BadArgument(f"{target} is not a user or guild!")
            else:
                target = ["guilds", guild.id, guild.name]
        else:
            target = ["humans", user.id, user.name]
        return target

    @commands.is_owner()
    @commands.group(invoke_without_command=True, help="The managerial command for the bot blacklist.")
    async def blacklist(self, ctx, target: int):
        target = await self.target_getter(target)
        with open("blacklist.json", "r") as blacklist_file:
            blacklist_update = json.load(blacklist_file)
            blacklist = blacklist_update["blacklist"]
            if target[1] in blacklist[target[0]]:
                added_or_removed = "removed from"
                blacklist_update["blacklist"][target[0]].remove(target[1])
            else:
                added_or_removed = "added to"
                blacklist_update["blacklist"][target[0]].append(target[1])
        with open("blacklist.json", "w") as file:
            json.dump(blacklist_update, file)
        await ctx.send(f"This {target[0].replace('s', '')} ({target[2]}) was {added_or_removed} the blacklist!")

    @commands.group(invoke_without_command=True, help="The managerial command group for git.")
    async def git(self, ctx):
        repo = pygit2.Repository('.git')
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), 10))
        formatted_commits = ""
        for c in commits:
            formatted_commits += f"\n{await format_commit(c)}"
        embed = embeds.twoembed("Most recent Git commits!", formatted_commits)
        await ctx.send(embed=embed)

    @commands.is_owner()
    @git.command(help="Syncs with the Git repository.")
    async def sync(self, ctx):
        async with ctx.channel.typing():
            embed = discord.Embed(title="Awaiting results...",
                                  description="Awaiting results from the GitHub repository.",
                                  color=self.bot.base_color)
            await ctx.send(embed=embed)
            proc = await asyncio.create_subprocess_shell(f"cd {self.bot.directory} & git pull",
                                                         stdout=asyncio.subprocess.PIPE,
                                                         stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            if stdout:
                embed.title = "STDOUT!"
                embed.description = f'{stdout.decode()}'
            if stderr:
                embed.title = "STDERR!"
                embed.description = f'{stderr.decode()}'
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))
