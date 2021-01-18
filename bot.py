import discord
import objectfile
import os
import yaml
import logging
import json
import subprocess
from datetime import datetime
from pur import update_requirements
from discord.ext import commands, tasks

async def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or(str("c+"))(bot, message)
    else:
        with open("databases/prefixes.json", "r") as f:
            servers = json.load(f)
        return commands.when_mentioned_or(str(servers[str(message.guild.id)]["prefix"]))(bot, message)


baselogger = logging.getLogger(__name__)
config = yaml.safe_load(open('config.yml'))
bot = commands.Bot(command_prefix=get_prefix, intents=objectfile.intents)
bot.command_num = 0
bot.owner_ids = config["owners"]
bot.snipe = {}
bot.editsnipe = {}
bot.launch_time = datetime.utcnow()
logging.basicConfig(format=f"[{datetime.utcnow()} %(name)s %(levelname)s] %(message)s", level=logging.INFO)
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

def has_admin():
    def predicate(ctx):
        guild = bot.get_guild(773318789617811526)
        role = guild.get_role(776253869038501918)
        if role in ctx.author.roles:
            return True
        else:
            return False
    return commands.check(predicate)


async def open_prefix_json():
    with open("databases/prefixes.json", "r") as f:
        return json.load(f)


async def change_prefix(guild, prefix):
    servers = await open_prefix_json()
    servers[str(guild.id)] = {}
    servers[str(guild.id)]["prefix"] = f"{prefix}"
    with open("databases/prefixes.json", "w") as f:
        json.dump(servers, f)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(str(f"{message.content} by {message.author} in #{message.channel} ({message.channel.id}) at {message.guild}"))
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    else:
        embed_var1 = discord.Embed(timestamp=datetime.utcnow(),
                                   title=f"Message deleted in #{message.channel}",
                                   description=f"The message author was <@!{message.author.id}>.",
                                   color=0x202225)
        embed_var1.add_field(name="Message", value=message.content, inline=False)
        embed_var1.set_thumbnail(url=message.author.avatar_url)
        bot.snipe[message.channel] = embed_var1
        if message.guild.id == 773318789617811526:
            logs = bot.get_channel(773318789617811526)
            await logs.send(embed=embed_var1)
        return embed_var1


@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    else:
        embed_var1 = discord.Embed(timestamp=datetime.utcnow(),
                                   title=f"Message edited in #{before.channel}",
                                   description=f"The message author was <@!{before.author.id}>.",
                                   color=0x202225)
        embed_var1.add_field(name="Message", value=before.content, inline=False)
        embed_var1.set_thumbnail(url=before.author.avatar_url)
        bot.editsnipe[before.channel] = embed_var1
        if before.guild.id != 773318789617811526:
            return embed_var1
        else:
            logs = bot.get_channel(773318789617811526)
            await logs.send(embed=embed_var1)
            return embed_var1


@bot.command()
async def snipe(ctx):
    if bot.snipe == {}:
        embed = objectfile.twoembed("No logged messages.",
                                    "Nobody sent any logged (deleted) messages "
                                    "in this channel!")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=bot.snipe[ctx.channel])


@snipe.error
async def snipe_error(error, ctx):
    if isinstance(error, KeyError):
        embed = objectfile.twoembed("No logged messages.",
                                    "Nobody sent any logged (deleted) messages "
                                    "in this channel!")
        await ctx.send(embed=embed)


@bot.command()
async def editsnipe(ctx):
    if bot.editsnipe == {}:
        embed = objectfile.twoembed("No logged messages.",
                                    "Nobody sent any logged (edited) messages "
                                    "in this channel!")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=bot.editsnipe[ctx.channel])


@editsnipe.error
async def editsnipe_error(self, error, ctx):
    if isinstance(error, KeyError):
        embed = objectfile.twoembed("No logged messages.",
                                    "Nobody sent any logged (deleted) messages "
                                    "in this channel!")
        await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    servers = await open_prefix_json()
    if str(guild.id) not in servers:
        await change_prefix(guild, "c+")
    else:
        return


@commands.group()
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
        servers = await open_prefix_json()
        embed = objectfile.twoembed("This server's prefix!",
                                    str(servers[str(ctx.guild.id)]["prefix"]))
        await ctx.send(embed=embed)


@prefix.command()
async def change(ctx, *, prefix: str = None):
    if ctx.author.guild_permissions.manage_guild or ctx.author is ctx.guild.owner or ctx.author.guild_permissions.administrator:
        if prefix is None:
            await ctx.send(embed=objectfile.newfailembed("Please specify a prefix.",
                                                         f"<@{ctx.author.id}>, please give a prefix!"))
        else:
            await change_prefix(ctx.guild, prefix)
            await ctx.send(embed=objectfile.twoembed("Updated this server's prefix.",
                                                     f"New prefix: {prefix}"))
    else:
        await ctx.send(embed=objectfile.newfailembed("Insufficient permissions!",
                                                     "You must have manage server or administrator."))


@tasks.loop(minutes=5)
async def status():
    guilds = "{:,}".format((len(list(bot.guilds))))
    members = "{:,}".format(len(bot.users))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"discord.gg/H5cBqhy4RD - {guilds} servers and {members}"
                                                             f" members!"))


@bot.event
async def on_ready():
    print('Compass is online!')
    channel = bot.get_channel(777248014460125184)
    embed = discord.Embed(colour=discord.Colour.from_rgb(0, 209, 24),
                          title='The bot is on', description=f"Compass is online!")
    await channel.send(embed=embed)
    print(str(bot.guilds))
    status.start()
    print([x[0]['message'] for x in update_requirements(input_file='requirements.txt').values()])


@commands.is_owner()
@bot.command(aliases=["stop"], hidden=True)
async def shutdown(ctx):
    author = ctx.message.author

    embed = discord.Embed(title="Shutting down...", colour=discord.Colour.from_rgb(211, 0, 0),
                          description=f"Bot shutdown ordered by {author}.")
    await ctx.send(embed=embed)

    channel = bot.get_channel(777248014460125184)
    embed = discord.Embed(title="Bye bye bot.", colour=discord.Colour.from_rgb(211, 0, 0),
                          description=f"Compass is being shutdown by {author}.")
    await channel.send(embed=embed)

    await bot.close()


@commands.is_owner()
@bot.command(hidden=True)
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
@bot.command(hidden=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    baselogger.info(f'Unoaded {extension}')
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
@bot.command(hidden=True)
async def restartallcogs(ctx):
    for filename in os.listdir('./cogs'):
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
@bot.command(hidden=True)
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
        if command.qualified_name == "help":
            pass
        else:
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
                embed.add_field(name=cog_name, value=str(command_signatures).replace("[", "").replace("]", "").replace("'", "").replace("None,", ""), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        baselogger.info(f"Loading cog cogs.{filename[:-3]}")

bot.load_extension("jishaku")
baselogger.info(f"Loading cog jishaku (outside of main folder)")
bot.run(config['token'])
