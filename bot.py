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

import discord
import objectfile
import os
import yaml
import logging
from datetime import datetime
from pur import update_requirements
from discord.ext import commands, tasks

async def get_prefix(bot, message):
    if message.guild is not None and message.guild.id == 336642139381301249:
        prefix = "c+"
    else:
        prefix = "c!"
    return commands.when_mentioned_or(str(prefix))(bot, message)

baselogger = logging.getLogger(__name__)
config = yaml.safe_load(open('config.yml'))
bot = commands.Bot(command_prefix=get_prefix, intents=objectfile.intents)
bot.command_num = 0
bot.owner_ids = config["owners"]
bot.launch_time = datetime.utcnow()
blacklisted = []
logging.basicConfig(format=f"[{datetime.utcnow()} %(name)s %(levelname)s] %(message)s", level=logging.INFO)
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

def has_admin():
    def predicate(ctx):
        guild = bot.get_guild(738530998001860629)
        role = guild.get_role(793211817174237215)
        list_of_ids = []
        for member in role.members:
            list_of_ids.append(member.id)
        if ctx.author.id in list_of_ids:
            return True
        else:
            return False
    return commands.check(predicate)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(str(f"{message.content} by {message.author} in #{message.channel} ({message.channel.id}) at {message.guild}"))
    await bot.process_commands(message)

@tasks.loop(minutes=5)
async def status():
    guilds = "{:,}".format((len(list(bot.guilds))))
    members = "{:,}".format(len(bot.users))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"discord.gg/SymdusT - {guilds} servers and {members}"
                                                             f" members!"))


@bot.event
async def on_ready():
    print('Compass is online!')
    channel = bot.get_channel(801974572244140033)
    embed = discord.Embed(colour=discord.Colour.from_rgb(0, 209, 24),
                          title='The bot is on', description=f"Compass is online!")
    await channel.send(embed=embed)
    print(str(bot.guilds))
    status.start()
    print([x[0]['message'] for x in update_requirements(input_file='requirements.txt').values()])


@commands.is_owner()
@bot.command(aliases=["stop"])
async def shutdown(ctx):
    author = ctx.message.author
    embed = discord.Embed(title="Shutting down...", colour=discord.Colour.from_rgb(211, 0, 0),
                          description=f"Bot shutdown ordered by {author}.")
    await ctx.send(embed=embed)
    channel = bot.get_channel(801974572244140033)
    embed = discord.Embed(title="Bye bye bot.", colour=discord.Colour.from_rgb(211, 0, 0),
                          description=f"Compass is being shutdown by {author}.")
    await channel.send(embed=embed)
    await bot.close()


@commands.is_owner()
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    baselogger.info(f'Loaded {extension}')
    author = ctx.message.author
    embed = discord.Embed(title="Cog Loaded", description=f"Specified cog {extension} loaded by {author}.",
                          colour=discord.Colour.from_rgb(0, 209, 24))
    await ctx.send(embed=embed)


@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title="Missing a Cog!",
                              description=f"{author}, you must provide a cog to load!", inline=False)
        await ctx.send(embed=embed)


@commands.is_owner()
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    baselogger.info(f'Unloaded {extension}')
    author = ctx.message.author
    embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title='Cog Unloaded',
                          description=f"Specified cog {extension} unloaded by {author}.")
    await ctx.send(embed=embed)


@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0))
        embed.add_field(name="Missing a Cog!", value=f"{author}, you must provide a cog to unload!", inline=False)
        await ctx.send(embed=embed)


@commands.is_owner()
@bot.command()
async def restartallcogs(ctx):
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.reload_extension(f'cogs.{filename[:-3]}')
    baselogger.info("Restarted all cogs")
    embed = objectfile.twoembed('Cog Restarted',
                                f"All cogs restarted by {ctx.message.author}.")
    await ctx.send(embed=embed)


@commands.is_owner()
@bot.command(hidden=True)
async def pull(ctx):
    await ctx.send("This might take a bit, so be patient.")
    async with ctx.channel.typing():
        await ctx.invoke((bot.get_command("jsk").callback)(bot.get_cog("Jishaku"), ctx, argument="git pull"))
        embed = objectfile.twoembed("Pulled from GitHub.",
                                    "Pulled from Github and reloaded every cog automatically.")
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                bot.reload_extension(f"cogs.{file[:-3]}")
    await ctx.send(embed=embed)


@commands.is_owner()
@bot.command(hidden=True)
async def push(ctx, *, arg):
    async with ctx.channel.typing():
        await ctx.send("This might take a bit, so be patient.")
        await ctx.invoke(bot.get_command(f'jsk git commit -a -m "{arg}" && git push'))
        embed = objectfile.twoembed("Pushed to Github.", "Pushed all changed files to GitHub.")
        await ctx.send(embed=embed)


@commands.is_owner()
@bot.command()
async def restartcog(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    baselogger.info(f'Specified cog {extension} restarted')
    author = ctx.message.author
    embed = objectfile.twoembed('Cog Restarted',
                                f"Specified cog {extension} restarted by {author}.")
    await ctx.send(embed=embed)


@restartcog.error
async def restartcog_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0))
        embed.add_field(name="Missing a Cog!", value=f"{author}, you must provide a cog to restart!", inline=False)
        await ctx.send(embed=embed)


class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"``{command.qualified_name}``"

    async def send_bot_help(self, mapping):
        legitsi = bot.get_user(184145857526890506)
        antonio = bot.get_user(210473676339019776)
        embed = discord.Embed(title="Help", description=f"{self.clean_prefix} is this server's prefix.\n"
                                                        f"**__Credits__**\n"
                                                        f"<@{legitsi.id}> ({legitsi.name}#{legitsi.discriminator}) for giving me DHC.\n"
                                                        f"<@{antonio.id}> ({antonio.name}#{antonio.discriminator}) for making the logo.", color=0x202225)
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Other")
                embed.add_field(name=cog_name, value=str(command_signatures).replace("[", "").replace("]", "").replace("'", ""), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        baselogger.info(f"Loading cog cogs.{filename[:-3]}")

bot.load_extension("jishaku")
baselogger.info(f"Loading cog jishaku (outside of main folder)")
bot.run(config['token'])
