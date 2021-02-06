# MIT License
#
# Copyright (c) 2021 Compass
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import math
import discord
import psutil
import wikipedia
import traceback
import objectfile
import logging
import yaml
import aiohttp
import asyncio
from datetime import datetime
from github import Github
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))
logging.basicConfig(format=f"[{datetime.utcnow()} %(name)s %(levelname)s] %(message)s", level=logging.ERROR)
logger = logging.getLogger(__name__)
g = Github(str(config['githubkey']))


class Errors(commands.Cog):
    def __init__(self, bot):
        self.process = psutil.Process()
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, asyncio.TimeoutError, discord.errors.HTTPException)
        error = getattr(error, 'original', error)
        if ctx.command.qualified_name == "about":
            return
        if isinstance(error, ignored):
            return
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=objectfile.newfailembed(f"Check failed!",
                                                                error))
        if isinstance(error, commands.NotOwner):
            await ctx.send(embed=objectfile.you_cant_use_this())
            return
        if isinstance(error, commands.CommandOnCooldown):
            num = math.ceil(error.retry_after)
            seconds = num
            minutes = round(num / 60)
            total = f"{seconds:,.2f} seconds ({minutes} minutes)."
            await ctx.send(embed=objectfile.newfailembed(f"Try again in {total}",
                                                         f"Cool down bro!"))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            author = ctx.message.author
            embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0))
            embed.set_author(name=f"{author}, you don't have a required argument.")
            embed.add_field(name="You'll need to add something at the end.", value=f"Example: {ctx.prefix}unload help")
            return
        if isinstance(error, wikipedia.exceptions.DisambiguationError):
            embed = objectfile.twoembed("That sent you to a disambiguation page.", error)
            await ctx.send(embed=embed)
            return
        if isinstance(error, wikipedia.exceptions.RedirectError):
            embed = objectfile.twoembed("That sent you to a redirect page.", error)
            await ctx.send(embed=embed)
            return
        if isinstance(error, wikipedia.exceptions.HTTPTimeoutError):
            embed = objectfile.failembed("The servers timed out.", "This is out of our control, sorry.",
                                         "We hope it'll get back on!")
            await ctx.send(embed=embed)
        if isinstance(error, wikipedia.exceptions.PageError):
            embed = objectfile.failembed("This page doesn't exist.", "Shit.",
                                         "Try searching something else!")
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MemberNotFound):
            embed = objectfile.twoembed(error,
                                        "Try again with someone else!")
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingPermissions):
            embed = objectfile.twoembed("I don't have perms or I was hierarchy'd.",
                                        "Give me permissions pwease!")
            await ctx.send(embed=embed)
        if isinstance(error, aiohttp.ClientError):
            await ctx.send(embed=objectfile.twoembed(f"Client error raised!",
                                                     f"Try again.\n"
                                                     f"If this is a persistent issue, join the support server at {ctx.prefix}about"
                                                     f" and report the bug."))
        else:
            # Github Issues
            channel = self.bot.get_channel(801972292837703708)
            traceback_text = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            repo = g.get_repo(f"Compass-Bot-Team/Compass")
            issue_url_but_what = repo.create_issue(title=f"Error in {ctx.command}.", assignee="DontTreadOnGerman",
                                                   body=f"{traceback_text}\n\n{logger.exception(error)}")
            issue_url = issue_url_but_what.url
            embed1 = discord.Embed(timestamp=datetime.utcnow(),
                                  colour=discord.Colour.from_rgb(211, 0, 0), title=f"Error in {ctx.command}!",
                                  description=f"```py\n{traceback_text}\n```\n\n{logger.exception(error)}")
            embed2 = discord.Embed(timestamp=datetime.utcnow(),
                                  colour=discord.Colour.from_rgb(211, 0, 0), title=f"Error in {ctx.command}!",
                                  description=f"```py\n{error}\n```\n\n{logger.exception(error)}")
            embed1.set_author(name="There was an error.")
            embed2.set_author(name="There was an error.")
            embed1.add_field(name="Issue URL", value=str(issue_url).replace("api.", "").replace("repos/", ""), inline=False)
            embed2.add_field(name="Issue URL", value=str(issue_url).replace("api.", "").replace("repos/", ""), inline=False)
            await channel.send(embed=embed1)
            await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Errors(bot))
