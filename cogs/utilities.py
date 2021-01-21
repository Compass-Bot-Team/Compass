import discord
import objectfile
import datetime
import validators
import sqlite3
import typing
import time
import re
import inspect
import platform
import psutil
import asyncio
import pkg_resources
import os
from objectfile import valids as valids
from datetime import datetime
from discord.ext import commands

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            time += time_dict[k]*float(v)
            return time

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.command_num = bot.command_num
        self.bot.launch_time = bot.launch_time
        self.process = psutil.Process()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_num += 1

    async def uptime(self):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_total = []
        if days != 0:
            uptime_total.append(f"{days} days")
        if hours != 0:
            uptime_total.append(f"{hours} hours")
        if minutes != 0:
            uptime_total.append(f"{minutes} minutes")
        if seconds != 0:
            uptime_total.append(f"{seconds} seconds")
        return str(uptime_total).replace("[", "").replace("]", "").replace("'", "")

    @commands.command()
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=objectfile.twoembed("Pinging...",
                                                           "Sit tight!"))
        end = time.perf_counter()
        start1 = time.perf_counter()
        async with ctx.channel.typing():
            pass
        end1 = time.perf_counter()
        duration = round((end - start) * 1000)
        typing = round((end1 - start1) * 1000)
        api_latency = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=0x202225, title="Pong!")
        embed.add_field(name="Messages", value=str(duration) + "ms", inline=True)
        embed.add_field(name="Typing", value=str(typing) + "ms")
        embed.add_field(name="API latency", value=str(api_latency) + "ms", inline=True)
        await message.edit(embed=embed)
        return

    @commands.command(aliases=["stats", "analytics"])
    async def about(self, ctx):
        cogs_list = str(list(map(str, self.bot.cogs))).replace(']', '').replace('[', '').replace("'", '')
        embed = objectfile.twoembed(f"About",
                                    f"Owner: DTOG#0001 721029142602056328\n"
                                    f"Uptime: {await self.uptime()}\n")
        servers = "{:,}".format(len(list(self.bot.guilds)))
        users = "{:,}".format(len(self.bot.users))
        command_alt = "{:,}".format(self.bot.command_num)
        objectfile.add_field(embed, "Stats", f"Cogs: {len(self.bot.cogs)} ({cogs_list})\n"
                                             f"Servers: {servers}\n"
                                             f"Members: {users}\n"
                                             f"Commands: {command_alt}", False)
        objectfile.add_field(embed, "Operating Stats",
                             f"Memory Usage: {round(self.process.memory_full_info().uss / 1024 ** 2)}mb\n"
                             f"CPU Usage: {round(self.process.cpu_percent() / psutil.cpu_count())}%\n"
                             f"Operating System: {platform.system()}", False)
        objectfile.add_field(embed, "Links",
                             f"Invite me [here!](https://discord.com/oauth2/authorize?client_id=769308147662979122&permissions=2147352567&scope=bot)\n"
                             f"Go to my GitHub [here!](https://github.com/Compass-Bot-Team/Compass)\n"
                             f"View my website + future dashboard [here!](https://compasswebsite.dev)\n"
                             f"Join the support server [here!](https://discord.gg/H5cBqhy4RD)", False)
        embed.set_footer(text=f"Made in discord.py {pkg_resources.get_distribution('discord.py').version}!")
        await ctx.send(embed=embed)

    @commands.command()
    async def addquote(self, ctx, *, args):
        message_success = objectfile.successembed("Quote added",
                                                  "You can now pull your quote.",
                                                  "People can be inspired by you!")
        message_error = objectfile.failembed("Nope!",
                                             "You don't have perms.",
                                             "Contact <@721029142602056328> for access to this command.")
        readfile = open("databases/quotes.txt", "r")
        if args in readfile.read():
            await ctx.send(embed=objectfile.failembed("This quote is already in the database....",
                                                      "Change it up or something.",
                                                      "Or it won't be added!"))
        else:
            if ctx.message.author.id in valids:
                write = open("databases/quotes.txt", "a")
                write.write(f"\n{args} |{ctx.author}")
                write.close()
                await ctx.send(embed=message_success)
            else:
                await ctx.send(embed=message_error)
        readfile.close()

    @commands.command()
    async def addmeme(self, ctx, *, args):
        message_success = objectfile.successembed("Quote added",
                                                  "You can now pull your meme.",
                                                  "People can... laugh at you?")
        message_error = objectfile.failembed("Nope!",
                                             "You don't have perms, or it's not a link (hence unlaughable.)",
                                             "Contact <@721029142602056328> for access to this command.")
        db = sqlite3.connect('databases/memes.db')
        c = db.cursor()
        data = c.fetchall()
        if args in data:
            await ctx.send(embed=objectfile.failembed("This meme is already in the database....",
                                                      "Change it up or something.",
                                                      "Or it won't be added!"))
            db.close()
        else:
            if ctx.message.author.id in objectfile.memevalids and validators.url(args):
                conn = sqlite3.connect('databases/memes.db')
                c = conn.cursor()
                c.execute(f"INSERT INTO Memes VALUES ('{args}')")
                conn.commit()
                conn.close()
                await ctx.send(embed=message_success)
            else:
                await ctx.send(embed=message_error)

    @commands.command(name="add8ballresponse")
    async def _add8ballresponse(self, ctx, *, args):
        message_success = objectfile.successembed("8ball response added",
                                                  "You can now pull your response.",
                                                  "Just try it!")
        message_error = objectfile.failembed("Nope!",
                                             "You don't have perms.",
                                             "Contact <@721029142602056328> for access to this command.")
        db = sqlite3.connect('databases/8ballresponses.db')
        c = db.cursor()
        data = c.fetchall()
        if args in data:
            await ctx.send(embed=objectfile.failembed("This response is already in the database....",
                                                      "Change it up or something.",
                                                      "Or it won't be added!"))
        else:
            if ctx.message.author.id in valids:
                conn = sqlite3.connect('databases/8ballresponses.db')
                c = conn.cursor()
                c.execute(f"INSERT INTO ballresponses VALUES ('{args}')")
                conn.commit()
                conn.close()
                await ctx.send(embed=message_success)
            else:
                await ctx.send(embed=message_error)

    @commands.command(name="addeatresponse")
    async def addeatresponse(self, ctx, *, args):
        message_success = objectfile.successembed("Eat response added",
                                                  "You can now eat something.",
                                                  "Just try it!")
        message_error = objectfile.failembed("Nope!",
                                             "You don't have perms.",
                                             "Contact <@721029142602056328> for access to this command.")
        db = sqlite3.connect('databases/eatresponses.db')
        c = db.cursor()
        data = c.fetchall()
        if args in data:
            await ctx.send(embed=objectfile.failembed("This response is already in the database....",
                                                      "Change it up or something.",
                                                      "Or it won't be added!"))
        else:
            if ctx.message.author.id in valids:
                conn = sqlite3.connect('databases/eatresponses.db')
                c = conn.cursor()
                c.execute(f"INSERT INTO eatresponses VALUES ('{args}')")
                conn.commit()
                conn.close()
                await ctx.send(embed=message_success)
            else:
                await ctx.send(embed=message_error)

    @commands.command()
    async def amiwhitelisted(self, ctx):
        validusers = objectfile.valids
        whitelistedyes = objectfile.successembed("You're whitelisted!",
                                                 "Congrats.",
                                                 "Go nuts!")
        whitelistedno = objectfile.failembed("You're not whitelisted!",
                                             "You're a casual.",
                                             "Contact <@721029142602056328> for access to whitelist commands.")
        if ctx.message.author.id in validusers:
            await ctx.send(embed=whitelistedyes)
        else:
            await ctx.send(embed=whitelistedno)

    @commands.command()
    async def suggest(self, ctx, *, suggestion=None):
        if ctx.message.author.id in objectfile.blacklistedusers:
            await ctx.send(embed=objectfile.blacklisted)
        else:
            if suggestion is None:
                await ctx.send(embed=objectfile.failembed("You don't have a suggestion?",
                                                          "You need to suggest something!",
                                                          "Example: compass!suggest blablablah"))
            else:
                current_time = datetime.datetime.now()
                author = ctx.message.author
                author_avatar = ctx.message.author.avatar_url
                server = ctx.message.guild
                suggestion = suggestion
                channel = ctx.message.channel
                suggestion_chat = self.bot.get_channel(777248717400571934)
                await ctx.send(embed=objectfile.successembed("Suggestion processed!",
                                                             "We'll get back to you when your suggestion is in.",
                                                             f"{suggestion}"))

                embed = discord.Embed(color=0x202225, title="New suggestion!")
                embed.set_thumbnail(url=f"{author_avatar}")
                embed.add_field(name=f"Suggestion by {author}",
                                value=f"{suggestion}\n**Server:** {server}\n**Channel:** {channel}", inline=False)
                embed.set_footer(text=f"{current_time}")
                send = await suggestion_chat.send(embed=embed)

    @commands.command()
    async def user(self, ctx, user: typing.Union[discord.Member, discord.User] = None):
        if user is None:
            member = ctx.message.author
        else:
            member = user
        embed = discord.Embed(color=0x202225,
                              title=f"{str(member)} ({str(member.display_name)})")
        embed.set_thumbnail(url=str(member.avatar_url))
        embed.add_field(name="ID", value=str(member.id), inline=False)
        embed.add_field(name="Status", value=f"{str(member.status).title()}", inline=False)
        embed.add_field(name="On Mobile", value=str(member.is_on_mobile()), inline=False)
        embed.add_field(name="Created At", value=str(member.created_at), inline=True)
        embed.add_field(name="Joined At", value=str(member.joined_at), inline=True)
        list_of_roles = []
        for role in member.roles:
            if role.name == "@everyone":
                list_of_roles.append(f"{role.name}")
            else:
                list_of_roles.append(f"<@&{role.id}>")
        embed.add_field(name=f"Roles ({len(member.roles)})", value=str(list_of_roles).replace("[", "").replace("]", "").replace("'", ""), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        server = ctx.message.guild
        embed = discord.Embed(color=0x202225,
                              title=str(server))
        embed.set_thumbnail(url=str(server.icon_url))
        embed.add_field(name="ID", value=str(server.id), inline=True)
        embed.add_field(name="Owner", value=str(server.owner), inline=True)
        embed.add_field(name="Created At", value=str(server.created_at), inline=True)
        embed.add_field(name="Members", value="{:,}".format(len(server.members)), inline=True)
        embed.add_field(name="Bots", value="{:,}".format(sum(m.bot for m in server.members)), inline=True)
        embed.add_field(name="Humans", value="{:,}".format(sum(not m.bot for m in server.members)), inline=True)
        embed.add_field(name="Role Count", value="{:,}".format(len(server.roles)), inline=True)
        if server.premium_subscription_count > 0:
            embed.add_field(name="Boosts", value=f"Level {str(server.premium_tier)} "
                                                 f"({str(server.premium_subscription_count)} boosts)", inline=True)
        if server.description is not None:
            embed.add_field(name="Description", value=str(server.description), inline=False)
        embed.set_image(url=str(server.banner_url))
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.message.author
        embed = objectfile.twoembed(f"{user}'s avatar!",
                                    f"[URL]({user.avatar_url})")
        embed.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)

    @commands.group()
    async def poll(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=objectfile.twoembed("The two sub commands for poll are;",
                                                     f"{ctx.prefix}poll classic or {ctx.prefix}poll number [1-10]!"))

    @poll.command()
    async def classic(self, ctx, *, question=None):
        base = ""
        if question is None:
            base += "N/A"
        else:
            base += f"{question}"
        embed = objectfile.mainembed(f"Question asked by {ctx.message.author}!", f"{base}",
                                     "<:green_square:779529584201695272> = Yes\n<:yellow_square:779529584201695272> = "
                                     "Neutral\n<:red_square:779529584201695272> = "
                                     "No\n<:purple_square:779530441450848277> = "
                                     "Other\n<:grey_question:779529584201695272> = Maybe")
        embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
        msg = await ctx.send(embed=embed)
        await objectfile.poll_classic(msg)

    @poll.command(name="number")
    async def number(self, ctx, num: int = None):
        await objectfile.number_poll(ctx.message, num)

    async def timer(self, second):
        if second == 0:
            embed = objectfile.twoembed(f"Timer over.",
                                        f"oh shit")
        else:
            embed = objectfile.twoembed(f"{time}.",
                                        f"oh shit")
        await asyncio.sleep(1)
        return embed

    @commands.command()
    async def timer(self, ctx, time: int):
        second = time
        seconds_preserved = time
        message = await ctx.send(embed=await self.timer(second))
        second += seconds_preserved
        for _ in range(seconds_preserved):
            second -= 1
        if second % 10 == 0:
            await message.edit(embed=await self.timer(second))

    @commands.command()
    async def source(self, ctx, *, command:str=None):
        # This command was mostly ripped from R-Danny (but not all of it.)
        # This is allowed under mozilla license.
        url = "https://github.com/Compass-Bot-Team/Compass"
        branch = "main"
        if command is None:
            return await ctx.send(embed=objectfile.twoembed("My source!",
                                                            url))
        else:
            if command == 'help':
                src = type(self.bot.help_command)
                module = src.__module__
                filename = inspect.getsourcefile(src)
            else:
                obj = self.bot.get_command(command.replace('.', ' '))
                if obj is None:
                    return await ctx.send(url)
                src = obj.callback.__code__
                module = obj.callback.__module__
                filename = src.co_filename
        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith('discord'):
            location = os.path.relpath(filename).replace('\\', '/')
        else:
            location = module.replace('.', '/') + '.py'
        await ctx.send(embed=objectfile.twoembed(f"Source for {command}!",
                                                 f'{url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'))

def setup(bot):
    bot.add_cog(Utilities(bot))
