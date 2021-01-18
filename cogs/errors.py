import datetime
import math
import discord
import psutil
import wikipedia
import objectfile
import logging
import yaml
import aiohttp
import asyncio
from datetime import datetime
from .music import music_commands
from .apis import country_commands as countries_country_commands
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
        if ctx.command.qualified_name == "tts":
            return
        else:
            if ctx.command.qualified_name not in countries_country_commands or music_commands:
                if hasattr(ctx.command, 'on_error'):
                    return
                cog = ctx.cog
                if cog:
                    if cog._get_overridden_method(cog.cog_command_error) is not None:
                        return
                ignored = (commands.CommandNotFound, asyncio.TimeoutError)
                error = getattr(error, 'original', error)
                if isinstance(error, ignored):
                    return
                if isinstance(error, commands.NotOwner):
                    await ctx.send(embed=objectfile.you_cant_use_this())
                    return
                if isinstance(error, commands.CommandOnCooldown):
                    num = math.ceil(error.retry_after)
                    seconds = num
                    minutes = round(num /  60)
                    total = "{:,} seconds ({:,} minutes).".format(seconds, minutes)
                    await ctx.send(embed=objectfile.failembed(f"This command is on cooldown!",
                                                              f"Try again in {total}",
                                                              "too fast for me"))
                    return
                if isinstance(error, commands.MissingRequiredArgument):
                    author = ctx.message.author
                    embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0))
                    embed.set_author(name=f"{author}, you don't have a required argument.")
                    embed.add_field(name="You'll need to add something at the end.", value=f"Example: compass!unload help")
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
                    repo = g.get_repo(f"Compass-Bot-Team/Compass")
                    issue_url_but_what = repo.create_issue(title=f"Error in {ctx.command}.", assignee="DontTreadOnGerman",
                                                           body=f"{error}\n\n{logger.exception(error)}")
                    issue_url = issue_url_but_what.url

                    channel = self.bot.get_channel(777226053105614860)
                    author = ctx.message.author

                    embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title=f"Error in {ctx.command}!",
                                          description=f"{error}\n\n{logger.exception(error)}")
                    embed.set_author(name="There was an error.")
                    embed.add_field(name="Server", value=f"{ctx.guild.id}", inline=True)
                    embed.add_field(name="Issue URL", value=str(issue_url).replace("api.", "").replace("repos/", ""), inline=False)
                    embed.timestamp = datetime.now()
                    await channel.send(embed=embed)

                    embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title=f"{author}, my bad.")
                    embed.add_field(name=f"Error in command {ctx.command}", value=f"```py\n{error}\n\n{logger.exception(error)}```", inline=True)
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Errors(bot))
