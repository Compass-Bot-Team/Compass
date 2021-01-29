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
import datetime
import typing
import time
import inspect
import platform
import psutil
import aiosqlite
import asyncio
import pkg_resources
import os
from bot import has_admin
from .server import blacklisted_or_not
from datetime import datetime
from discord.ext import commands

checkfail = objectfile.newfailembed("You aren't a bot admin!",
                                    "Try harder.")

support_channel_id = 803375502433189888

class Bot(commands.Converter):
    async def convert(self, ctx, bot: typing.Union[discord.User, discord.Member]):
        user = await ctx.bot.fetch_user(bot.id)
        if not user.bot:
            return None
        return user

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.command_num = bot.command_num
        self.bot.launch_time = bot.launch_time
        self.process = psutil.Process()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_num += 1

    @has_admin()
    @commands.command()
    async def addmeme(self, ctx, *, link:str):
        try:
            async with aiosqlite.connect('compassdb.db') as db:
                await db.execute(f"""INSERT INTO Memes VALUES ("{link}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")
        except aiosqlite.Error:
            async with aiosqlite.connect('compassdb.db') as db:
                await db.execute('''CREATE TABLE Memes (link, author)''')
                await asyncio.sleep(0.1)
                await db.execute(f"""INSERT INTO Memes VALUES ("{link}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")

    @has_admin()
    @commands.command()
    async def addquote(self, ctx, *, quote:str):
        try:
            async with aiosqlite.connect('compassdb.db') as db:
                await db.execute(f"""INSERT INTO Quotes VALUES ("{quote}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")
        except aiosqlite.Error:
            async with aiosqlite.connect('compassdb.db') as db:
                await db.execute('''CREATE TABLE Quotes (quote, author)''')
                await asyncio.sleep(0.1)
                await db.execute(f"""INSERT INTO Quotes VALUES ("{quote}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")

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

    async def typing_speed(self, ctx):
        start1 = time.perf_counter()
        async with ctx.channel.typing():
            pass
        end1 = time.perf_counter()
        return f"{round((end1 - start1) * 1000)}ms"

    async def db_speed(self):
        start2 = time.perf_counter()
        await aiosqlite.connect('compassdb.db')
        end2 = time.perf_counter()
        return f"{round((end2 - start2) * 1000)}ms"

    @commands.command()
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=objectfile.twoembed("Pinging...",
                                                           "Sit tight!"))
        end = time.perf_counter()
        embed = discord.Embed(colour=0x202225, title="Pong!", description=str(round((end - start) * 1000)) + "ms")
        embed.add_field(name="Websocket", value=str(round(self.bot.latency * 1000)) + "ms", inline=True)
        embed.add_field(name="Typing", value=await self.typing_speed(ctx), inline=True)
        embed.add_field(name="Database (Aiosqlite)", value=await self.db_speed(), inline=True)
        await message.edit(embed=embed)

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
                    return await ctx.send(embed=objectfile.twoembed("My source!",
                                                                    url))
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

    @blacklisted_or_not()
    @commands.command()
    async def support(self, ctx, *, question:str):
        try:
            support_channel = self.bot.get_channel(support_channel_id)
            embed = objectfile.twoembed(f"Question from {ctx.author}!",
                                        question)
            embed.add_field(name="Channel ID", value=ctx.channel.id, inline=True)
            embed.add_field(name="Author ID", value=ctx.author.id, inline=True)
            await support_channel.send(embed=embed)
            await ctx.send(embed=objectfile.twoembed("Sent to the support team!",
                                                     "Join the support server at [this link.](https://discord.gg/SymdusT)"))
        except commands.CheckFailure:
            await ctx.send(embed=objectfile.newfailembed("You're blacklisted!",
                                                         "Behave."))

    @has_admin()
    @commands.command()
    async def reply(self, ctx, channel:int, author:int, *, response:str):
        try:
            channel_redux = self.bot.get_channel(channel)
            await ctx.send("Success!")
            await channel_redux.send(f"<@{author}>", embed=objectfile.twoembed(f"Response from {ctx.author}!",response))
        except commands.CheckFailure:
            await ctx.send(embed=checkfail)

def setup(bot):
    bot.add_cog(Utilities(bot))
