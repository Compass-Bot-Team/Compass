# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import asyncio
import aiosqlite
from utils import useful_functions, embeds
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

    @shell.command(help="Runs SQL code.")
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


def setup(bot):
    bot.add_cog(Developer(bot))
