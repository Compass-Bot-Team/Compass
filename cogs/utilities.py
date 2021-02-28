# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import discord
import humanize
import pkg_resources
import sys
import psutil
import time
import aiosqlite
import typing
import inspect
import os
from utils import embeds, useful_functions, checks
from discord.ext import commands

support_channel_id = 803375502433189888


class Utilities(commands.Cog, description='All of the utility commands for the bot.'):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.memory = self.process.memory_full_info()
        self.version = sys.version_info

    @commands.command(help="All available statuses the bot uses.")
    async def statuses(self, ctx):
        status_list = ""
        async with aiosqlite.connect("storage.db") as db:
            async with db.execute("SELECT *, rowid FROM Statuses;") as cursor:
                while True:
                    try:
                        for _ in iter(int, 1):
                            info = await cursor.fetchone()
                            status_list += f"• {info[0]} (ID #{info[1]})\n"
                    except Exception:
                        break
        await ctx.send(embed=embeds.twoembed("All statuses!",
                                             status_list))

    @commands.Cog.listener()
    async def on_ready(self):
        useful_functions.logger.info("Bot cache configured.")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.command_num += 1
        member_dictionary = self.bot.command_users
        if ctx.author.id in member_dictionary:
            member_dictionary[ctx.author.id] += 1
        else:
            member_dictionary[ctx.author.id] = 1
        guild_dictionary = self.bot.command_guilds
        if ctx.guild is not None:
            if f"{ctx.guild} ({ctx.guild.id})" not in guild_dictionary:
                guild_dictionary[f"{ctx.guild} ({ctx.guild.id})"] = 1
            else:
                guild_dictionary[f"{ctx.guild} ({ctx.guild.id})"] += 1

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction("<:compass_bot_yes:809974729136930836>")

    @commands.Cog.listener()
    async def on_message(self, message):
        # just helping friends pls ignore this
        people = [574984194024013825, 210958048691224576]
        swears = ["fuck", "shit", "bitch", "bitches", "fucking", "fucker", "shitted", "shitting", "fucker",
                  "motherfucker", "dogshit", "bullshit", "ass", "faggot", "goddamn", "fag"]
        alt_lists = list(f"{swear}." for swear in swears) + list(f"{swear}," for swear in swears) + list(f"{swear}!" for swear in swears) + list(f"{swear}?" for swear in swears) + list(f"{swear}s" for swear in swears)
    #    for swear in alt_lists:
    #        alt_lists += list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in swear))))
        if message.author.id in people and message.content in alt_lists:
            await message.channel.send(f"<@{message.author.id}> STOP SWEARING <:TBK_witheredwojak:742475096366776370>")
        # ok now this is actually cache stuff below this line
        if message.author.bot or message.webhook_id is not None:
            return
        else:
            other_dictionary = self.bot.guild_senders
            if message.guild is not None:
                if f"{message.guild} ({message.guild.id})" not in other_dictionary:
                    other_dictionary[f"{message.guild} ({message.guild.id})"] = 1
                else:
                    other_dictionary[f"{message.guild} ({message.guild.id})"] += 1
            self.bot.message_num += 1
            member_dictionary = self.bot.message_senders
            if message.author.id in member_dictionary:
                member_dictionary[message.author.id] += 1
            else:
                member_dictionary[message.author.id] = 1

    @commands.is_owner()
    @commands.command(help="Adds a quote to the database of quotes. Admin only command.")
    async def addstatus(self, ctx, *, status: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        async with aiosqlite.connect("storage.db") as db:
            await db.execute(f"""INSERT INTO Statuses VALUES ("{status}");""")
            await db.commit()
            await ctx.send(f"Success!")

    @commands.command(aliases=["stats", "analytics"], help="Posts some cool information about the bot.")
    async def about(self, ctx):
        DTOG = self.bot.get_user(self.bot.config["owners"][0])
        Anto = self.bot.get_user(210473676339019776)
        LegitSi = self.bot.get_user(184145857526890506)
        embed = embeds.twoembed(f"About",
                                f"Owner: {DTOG} {DTOG.id}\n"
                                f"Bot Artist: {Anto} {Anto.id}\n"
                                f"Hurricane Man: {LegitSi} {LegitSi.id}\n"
                                f"Uptime: {await useful_functions.uptime(self.bot)}\n")
        embed.url = "https://www.github.com/Compass-Bot-Team/Compass"
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Compass-Bot-Team/Compass/main/github.png")
        stats_fields = {await useful_functions.users(self.bot): "Top Bot Users",
                        await useful_functions.noliferusers(self.bot): "Top No Lifers",
                        await useful_functions.guilds(self.bot): "Top Server Bot Users",
                        await useful_functions.noliferguilds(self.bot): "Top Server No Lifers"}
        field_inline_status = [True, True, False, False]
        field_count = 0
        for field in stats_fields:
            if field is not None:
                embed.add_field(name=stats_fields[field], value=field, inline=field_inline_status[field_count])
            field_count += 1
        embed.add_field(name="Stats", value=f"Cogs: {len(self.bot.cogs):,} ({await useful_functions.cogs(self.bot)})\n"
                                            f"Commands: {self.bot.command_num:,}\n"
                                            f"Messages: {self.bot.message_num:,}\n"
                                            f"Total Users: {len(self.bot.users):,}\n"
                                            f"Total Humans: {sum(not m.bot for m in self.bot.users):,}\n"
                                            f"Servers: {len(self.bot.guilds):,}", inline=False)
        embed.add_field(name="Operating Stats",
                        value=f"Memory Usage: {humanize.naturalsize(self.memory.rss)} physical, {humanize.naturalsize(self.memory.vms)} virtual, {humanize.naturalsize(self.memory.uss)} dedicated to the bot\n "
                              f"CPU Usage: {round(self.process.cpu_percent() / psutil.cpu_count(), 1)}%\n"
                              f"Operating System: {sys.platform}", inline=False)
        invite = "https://discord.com/oauth2/authorize?client_id=769308147662979122&permissions=2147352567&scope=bot"
        embed.add_field(name="Some Links", value=f"[Invite]({invite}) | [Support Server](https://discord.gg/SymdusT) | [GitHub](https://www.github.com/Compass-Bot-Team/Compass) | [Website](https://compasswebsite.dev)")
        embed.set_footer(text=f"Made in discord.py {pkg_resources.get_distribution('discord.py').version} + "
                              f"Python {self.version.major}.{self.version.minor}.{self.version.micro}!")
        await ctx.send(embed=embed)

    async def db_speed(self):
        start2 = time.perf_counter()
        await aiosqlite.connect('storage.db')
        end2 = time.perf_counter()
        return f"{round((end2 - start2) * 1000)}ms"

    @commands.command(help="Pong.")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send(embed=embeds.twoembed("Pinging...",
                                                       "Sit tight!"))
        end = time.perf_counter()
        embed = embeds.twoembed("Pong!", str(round((end - start) * 1000)) + "ms")
        embed.add_field(name="Websocket", value=str(round(self.bot.latency * 1000)) + "ms", inline=True)
        embed.add_field(name="SQL Database", value=await self.db_speed(), inline=True)
        await message.edit(embed=embed)

    @commands.command(aliases=['servermessages'], help='Shows the daily messages in the current guild.')
    async def guildmessages(self, ctx):
        _dict = self.bot.guild_senders
        if f"{ctx.guild} ({ctx.guild.id})" not in _dict:
            _dict[f"{ctx.guild} ({ctx.guild.id})"] = 0
        guild = f"{ctx.guild} ({ctx.guild.id})"
        embed = embeds.twoembed(f"Current standings for {ctx.guild}!",
                                f"""{_dict[guild]:,} human messages""")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(help="Shows information about a specified user.")
    async def user(self, ctx, user: typing.Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.message.author
        embed = discord.Embed(color=0x202225)
        if user.display_name == user.name:
            embed.title = f"{str(user)}"
        else:
            embed.title = f"{str(user)} ({str(user.display_name)})"
        embed.set_thumbnail(url=str(user.avatar_url))
        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(name="Status", value=f"{str(user.status).title()}", inline=False)
        embed.add_field(name="On Mobile", value=str(user.is_on_mobile()), inline=False)
        embed.add_field(name="Created At", value=str(user.created_at), inline=True)
        embed.add_field(name="Joined At", value=str(user.joined_at), inline=True)
        list_of_roles = []
        for role in user.roles:
            if role.name == "@everyone":
                list_of_roles.append(f"{role.name}")
            else:
                list_of_roles.append(f"<@&{role.id}>")
        embed.add_field(name=f"Roles ({len(user.roles)})",
                        value=str(list_of_roles).replace("[", "").replace("]", "").replace("'", ""), inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Shows information about the current server.")
    async def server(self, ctx):
        server = ctx.message.guild
        embed = discord.Embed(color=0x202225,
                              title=str(server))
        embed.set_thumbnail(url=str(server.icon_url))
        embed.add_field(name="ID", value=server.id, inline=True)
        embed.add_field(name="Owner", value=server.owner, inline=True)
        embed.add_field(name="Created At", value=str(server.created_at), inline=True)
        embed.add_field(name="Members", value=f"{server.members:,}", inline=True)
        embed.add_field(name="Bots", value=f"{sum(m.bot for m in server.members):,}", inline=True)
        embed.add_field(name="Humans", value=f"{sum(not m.bot for m in server.members):,}", inline=True)
        embed.add_field(name="Role Count", value=f"{len(server.roles):,}", inline=True)
        if server.premium_subscription_count > 0:
            embed.add_field(name="Boosts", value=f"Level {str(server.premium_tier)} "
                                                 f"({str(server.premium_subscription_count)} boosts)", inline=True)
        if server.description is not None:
            embed.add_field(name="Description", value=str(server.description), inline=False)
        embed.set_image(url=str(server.banner_url))
        await ctx.send(embed=embed)

    @commands.command(help="Posts a user's or your avatar.")
    async def avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.message.author
        embed = embeds.twoembed(f"{user}'s avatar!",
                                f"[URL]({user.avatar_url})")
        embed.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(help="Shows the GitHub URL of a command.")
    async def source(self, ctx, *, command: str = None):
        # This command was mostly ripped from R-Danny (but not all of it.)
        # This is allowed under mozilla license.
        url = "https://github.com/Compass-Bot-Team/Compass"
        branch = "rewrite"
        if command is None:
            return await ctx.send(embed=embeds.twoembed("My source!",
                                                        url))
        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            async with ctx.channel.typing():
                obj = self.bot.get_command(command.replace('.', ' '))
                if obj is None:
                    return await ctx.send(embed=embeds.twoembed("My source!",
                                                                url))
                src = obj.callback.__code__
                module = obj.callback.__module__
                filename = src.co_filename
            lines, firstlineno = inspect.getsourcelines(src)
            if not module.startswith('discord'):
                location = os.path.relpath(filename).replace('\\', '/')
            else:
                location = module.replace('.', '/') + '.py'
            await ctx.send(embed=embeds.twoembed(f"Source for {command}!",
                                                 f'{url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'))

    @commands.command(help="Sends a support question to the bot support team.")
    async def support(self, ctx, *, question: str):
        support_channel = self.bot.get_channel(support_channel_id)
        embed = embeds.twoembed(f"Question from {ctx.author}!",
                                question)
        embed.add_field(name="Channel ID", value=ctx.channel.id, inline=True)
        embed.add_field(name="Author ID", value=ctx.author.id, inline=True)
        await support_channel.send(embed=embed)
        await ctx.send(embed=embeds.twoembed("Sent to the support team!",
                                             "Join the support server at [this link.](https://discord.gg/SymdusT)"))

    @checks.has_admin()
    @commands.command(help="Replies to a support query. Owner only command.")
    async def reply(self, ctx, channel: int, author: int, *, response:str):
        await ctx.send("Success!")
        await self.bot.get_channel(channel).send(f"<@{author}>", embed=embeds.twoembed(f"Response from {ctx.author}!",response))

    @commands.group(invoke_without_command=True, help="Shows information about an invite.")
    async def invite(self, ctx, invite: discord.Invite):
        embed = discord.Embed(colour=0x202225, title=f"Information for {invite}!", description=f"Invite created by {invite.inviter}")
        embed.set_footer(text=f"Invite created at {invite.created_at}")
        embed.add_field(name="Invite Uses", value=invite.uses, inline=True)
        embed.add_field(name="Temporary Membership", value=invite.temporary, inline=True)
        embed.add_field(name="Revoked", value=invite.revoked, inline=True)
        embed.add_field(name="Invite Channel", value=f"<#{invite.channel.id}>", inline=True)
        embed.add_field(name="Invite Server", value=invite.guild.name, inline=True)
        if invite.max_age is not None:
            embed.add_field(name="Max Age in seconds", value=invite.max_age, inline=True)
        await ctx.send(embed=embed)

    @commands.command(help="Shows information about a specified bot.")
    async def bot(self, ctx, bot: typing.Union[discord.Member, discord.User]):
        if bot.bot:
            if bot in ctx.guild.members:
                embed = embeds.twoembed(f"Information about {bot}!",
                                        f"You can invite {bot} by [clicking here.](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions={bot.guild_permissions.value}&scope=bot)")
                embed.add_field(name="Bot Permissions", value=f"[{bot.guild_permissions.value}](https://discordapi.com/permissions.html#{bot.guild_permissions.value})", inline=True)
            else:
                embed = embeds.twoembed(f"Information about {bot}!",
                                        f"You can invite {bot} by [clicking here.](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=bot)")
            embed.set_thumbnail(url=bot.avatar_url)
            async with aiosqlite.connect('storage.db') as db:
                server = await db.execute(f"""SELECT server FROM SupportServers WHERE bot = "{bot.id}";""")
                grabbed_server = str(await server.fetchone()).replace("('", "").replace(")", "").replace("%27,", "").replace("',", "")
                embed.add_field(name="Support Server", value=grabbed_server.replace("None", "None (request a support server by joining [here.](https://discord.gg/SymdusT))"), inline=True)
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument("This isn't a bot!")

    @checks.has_admin()
    @commands.command(help="Adds a server to the bot server database. Admin only command.")
    async def addbotserver(self, ctx, server: str, bot: typing.Union[discord.User, discord.Member]):
        if bot.bot:
            async with aiosqlite.connect('storage.db') as db:
                await db.execute(f"""INSERT INTO SupportServers VALUES ("{server}", "{bot.id}");""")
                await db.commit()
            await ctx.send(f"Success!")
        else:
            await ctx.send("This is not a bot.")

    @commands.command(help="Shows information about a specified role.")
    async def role(self, ctx, *, role: discord.Role):
        query = f"""http://www.colourlovers.com/img/{hex(role.colour.value).replace("0x", "")}/100/100/"""
        embed = discord.Embed(colour=0x202225, title=f"Information about {role.name} (ID {role.id}!)")
        embed.set_thumbnail(url=query.replace("/img/0/100/100/", "/img/8B99A4/100/100/"))
        embed.add_field(name="Permissions", value=f"[{role.permissions.value}](https://discordapi.com/permissions.html#{role.permissions.value})", inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.add_field(name="Position", value=f"{role.position}/{len(ctx.guild.roles)}", inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Managed by 3rd party", value=role.managed, inline=True)
        embed.add_field(name="Is Managed", value=role.is_bot_managed(), inline=True)
        embed.add_field(name="Is the Boost Role", value=role.is_premium_subscriber(), inline=True)
        embed.add_field(name="Is an Integration", value=role.is_integration(), inline=True)
        embed.set_footer(text=f"Role created at {role.created_at}.")
        member_count = 0
        members = ""
        for member in role.members:
            if member_count == 0:
                members += f"<@{member.id}>"
            else:
                members += f", <@{member.id}>"
            member_count += 1
        try:
            embed.add_field(name=f"Role Members ({len(role.members)})", value=members, inline=False)
        except discord.errors.HTTPException:
            embed.add_field(name=f"Role Members ({len(role.members)})", value="There was too much to put here.", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
