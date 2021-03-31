# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import async_cleverbot
import discord
import typing
import mystbin
import datetime
import random
import aiosqlite
import asyncio
import pycountry
from utils import executors, embeds, hurricane_generator, useful_functions, checks
from discord.ext import commands

support_server_id = 738530998001860629
log_channel_id = 801972292837703708
support_channel_id = 801974601294020609
chatbot_channel_id = 801971149285883955


class Fun(commands.Cog, description='''All of the bot's fun commands.'''):
    def __init__(self, bot):
        self.bot = bot
        self.member_not_found_triggers = (TypeError, AttributeError)
        self.token = bot.config["githubkey"]
        self.bot.snipe = {}
        self.bot.editsnipe = {}
        self.mystbin = mystbin.Client()
        self.cleverbot = async_cleverbot.Cleverbot(self.bot.config['travitiakey'])

    async def get_chatbot_channels(self):
        await useful_functions.wait_until(self.bot)
        channels = []
        async with aiosqlite.connect(f"{self.bot.directory}/storage.db") as db:
            async with db.execute("SELECT *, rowid FROM ChatbotChannels;") as cursor:
                while True:
                    try:
                        for _ in iter(int, 1):
                            info = await cursor.fetchone()
                            channels.append(int(info[0]))
                    except Exception:
                        break
            return channels

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot or message.webhook_id is not None:
            return
        if message.channel.id not in list(await self.get_chatbot_channels()):
            return
        if len(message.content) < 3 or len(message.content) > 60:
            await message.channel.send(embed=embeds.failembed("All messages must be above 3 and below 60 characters!", "API limitations, sowwy."))
        else:
            async with message.channel.typing():
                request = await self.cleverbot.ask(str(message.content))
            await message.channel.send(embed=embeds.twoembed(f"My response!", request))

    async def check_if_opted_out(self, user):
        async with aiosqlite.connect("storage.db") as db:
            async with db.execute("SELECT User from OptOutUsers;") as cursor:
                while True:
                    try:
                        users = []
                        for _ in iter(int, 1):
                            info = await cursor.fetchone()
                            users.append(info[0])
                    except Exception:
                        break
        if str(user) in users:
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        else:
            if await self.check_if_opted_out(message.author.id) is True:
                title = "User opted out"
                description = "User opted out, they can opt in again if they want by running the 'snipe opt' command"
                thumbnail = None
            else:
                title = f"Message from {message.author} deleted!"
                description = message.content
                thumbnail = message.author.avatar_url
            embed = embeds.twoembed(title, description)
            embed.timestamp = datetime.datetime.utcnow()
            if thumbnail is not None:
                embed.set_thumbnail(url=thumbnail)
            self.bot.snipe[message.channel.id] = embed

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        else:
            if await self.check_if_opted_out(before.author.id) is True:
                title = "User opted out"
                description = "User opted out, they can opt in again if they want by running the 'snipe opt' command"
                thumbnail = None
            else:
                title = f"Message from {before.author} edited!"
                description = before.content
                thumbnail = before.author.avatar_url
            embed = embeds.twoembed(title, description)
            embed.timestamp = datetime.datetime.utcnow()
            if thumbnail is not None:
                embed.set_thumbnail(url=thumbnail)
            self.bot.editsnipe[before.channel.id] = embed

    @commands.command(help="Posts a random person in the message server.")
    async def someone(self, ctx):
        await ctx.send(embed=embeds.twoembed(f"{ctx.message.author}, here's someone.",
                                             f"<@{random.choice(ctx.guild.members).id}>"))

    @commands.group(invoke_without_command=True,
                    help="Posts the last deleted message in the channel.")
    async def snipe(self, ctx, *, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if ctx.author in channel.members:
            await ctx.send(embed=self.bot.snipe[channel.id])
        else:
            await ctx.send(embed=embeds.failembed("You can't view this channel!",
                                                  "Try a different channel."))

    @snipe.command(help="Manages the snipe opt out system.")
    async def opt(self, ctx):
        if await self.check_if_opted_out(ctx.author.id) is True:
            command = f"""INSERT INTO OptOutUsers VALUES ("{ctx.author.id}");"""
        else:
            command = f"""DELETE FROM OptOutUsers WHERE User = "{ctx.author.id}";"""
        async with aiosqlite.connect("storage.db") as connection:
            await connection.execute(command)
            await connection.commit()
            await ctx.send(command)


    @commands.command(help="Posts the last edited message in the channel.")
    async def editsnipe(self, ctx, *, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if ctx.author in channel.members:
            await ctx.send(embed=self.bot.editsnipe[channel.id])
        else:
            await ctx.send(embed=embeds.failembed("You can't view this channel!",
                                                  "Try a different channel."))

    @commands.command(help="Screenshots a website.")
    async def screenshot(self, ctx, *, url: str):
        await ctx.send(embed=embeds.imgembed("Website screenshotted!", f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}"))

    @commands.command(help="Posts a meme.")
    async def meme(self, ctx, id: int = None):
        if id is not None:
            query = f"SELECT *, rowid FROM Memes WHERE rowid = {id};"
        else:
            query = "SELECT *, rowid FROM Memes ORDER BY RANDOM() LIMIT 1;"
        async with aiosqlite.connect("storage.db") as db:
            async with db.execute(query) as cursor:
                get_info = await cursor.fetchone()
                author = get_info[1]
                rowid = get_info[2]
                user = self.bot.get_user(int(author))
                linkcalc = str(get_info[0]).replace("('", "").replace(")", "").replace("%27,", "").replace("',", "")
                await ctx.send(f"Your meme (ID {rowid}!)\nSubmitted by {user} ({user.id})\n\n{linkcalc}")

    @commands.command(help="Quotes something.")
    async def quote(self, ctx, id: int = None):
        if id is not None:
            query = f"SELECT *, rowid FROM Quotes WHERE rowid = {id};"
        else:
            query = "SELECT *, rowid FROM Quotes ORDER BY RANDOM() LIMIT 1;"
        async with aiosqlite.connect("storage.db") as db:
            async with db.execute(query) as cursor:
                get_info = await cursor.fetchone()
                rowid = get_info[2]
                author = get_info[1]
                quote = get_info[0]
                await ctx.send(embed=embeds.twoembed(f"Quote {rowid}",
                                                     f"> {quote}\n"
                                                     f"  - <@{author}>"))

    @checks.meme_quote_perms()
    @commands.command(help="Adds a meme to the database of memes. Admin only command.")
    async def addmeme(self, ctx, *, link: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        async with aiosqlite.connect('storage.db') as db:
            await db.execute(f"""INSERT INTO Memes VALUES ("{discord.utils.escape_mentions(link)}", "{ctx.author.id}");""")
            await db.commit()
        await ctx.send(f"Success!")

    @checks.meme_quote_perms()
    @commands.command(help="Adds a quote to the database of quotes. Admin only command.")
    async def addquote(self, ctx, *, quote: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        async with aiosqlite.connect('storage.db') as db:
            await db.execute(f"""INSERT INTO Quotes VALUES ("{discord.utils.escape_mentions(quote)}", "{ctx.author.id}");""")
            await db.commit()
            await ctx.send(f"Success!")

    @commands.command(help="Pastes something onto [mystb.in.](https://mystb.in)")
    async def mystbin(self, ctx, *, text: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        async with ctx.channel.typing():
            url = await self.mystbin.post(text, syntax="markdown")
        await ctx.send(embed=embeds.twoembed("Your mystb.in!",
                                             str(url)))

    @commands.command(help="Says something in TTS. But, you have to provide the something")
    async def tts(self, ctx, *, text: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        await ctx.send(file=discord.File(await self.bot.loop.run_in_executor(None, executors.tts, discord.utils.escape_mentions(text)), filename="tts.mp3"))

    @commands.group(help="Communicates with cleverbot.", invoke_without_command=True)
    async def chat(self, ctx, *, content: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        if content == f"{ctx.prefix}chat setup":
            return
        if len(content) < 3 or len(content) > 60:
            await ctx.send(embed=embeds.failembed("All messages must be above 3 and below 60 characters!",
                                                  "API limitations, sowwy."))
        else:
            chatbot = await self.cleverbot.ask(discord.utils.escape_mentions(str(content)))
            await ctx.send(embed=embeds.twoembed(f"My response!", chatbot))

    @commands.has_permissions(manage_guild=True)
    @chat.command(help="Adds or removes a chatbot channel. You can specify a channel but if you don't it defaults to the current channel")
    async def setup(self, ctx, *, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        channels = await self.get_chatbot_channels()
        if channel.id in channels:
            query = f"""DELETE FROM ChatbotChannels WHERE channel = "{channel.id}";"""
            returned = f"Deleted #{channel.name} from the database."
        else:
            query = f"""INSERT INTO ChatbotChannels VALUES ("{channel.id}");"""
            returned = f"Added #{channel.name} to the database."
        async with aiosqlite.connect("storage.db") as db:
            await db.execute(query)
            await db.commit()
        await ctx.send(embed=embeds.twoembed("Success!", returned))

    @commands.group(invoke_without_command=True, help="Says something.")
    async def say(self, ctx, *, content: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        embed = embeds.twoembed(f"Message from {ctx.author}!", discord.utils.escape_mentions(content))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @say.command(help="Says something in text form.")
    async def text(self, ctx, *, content: commands.clean_content(use_nicknames=False, fix_channel_mentions=True)):
        await ctx.send(discord.utils.escape_mentions(content))

    @commands.command(help="Generates a random hurricane season. This command only supports areas in the juristdiction of the National Hurricane Center/Central Pacific Hurricane Center."
                           "Valid years: 2021, 2022, 2023, 2024, 2025, 2026"
                           "Valid locations: Atlantic, Eastern Pacific, Central Pacific")
    async def generateseason(self, ctx, year: typing.Optional[int] = None, location: str = None):
        cpac_status = False
        if location is None:
            location = "Atlantic"
        elif location in hurricane_generator.atlantic_list:
            location = "Atlantic"
        elif location in hurricane_generator.epac_list:
            location = "Eastern Pacific"
        elif location in hurricane_generator.cpac_list:
            location = "Central Pacific"
            cpac_status = True
        else:
            raise commands.BadArgument("Invalid location!")
        list_of_years = [2021, 2022, 2023, 2024, 2025, 2026]
        if year is None:
            year = 2021
        if year not in list_of_years:
            raise commands.BadArgument("Invalid year!\nValid years: 2021, 2022, 2023, 2024, 2025, 2026")
        hurricane_list = await hurricane_generator.hurricane_list_calc(year, location)
        tropical_depression_list = hurricane_generator.numbers
        tropical_depressions = 0
        tropical_storms = 0
        hurricanes = 0
        major_hurricanes = 0
        la_nina_or_el_nino = random.choice(['La Nina', 'El Nino'])
        hurricane_amount = await hurricane_generator.hurricane_amount_calc(la_nina_or_el_nino, cpac_status)
        tropical_cyclones = ""
        for _ in range(hurricane_amount):
            chance = random.randint(1, 100)
            mph = random.choice(await hurricane_generator.acceptable(chance))
            kph = round(mph / 1.151)
            if mph < 39:
                name = tropical_depression_list[tropical_depressions]
                tropical_depressions += 1
            else:
                name = hurricane_list[tropical_storms]
                tropical_depressions += 1
                tropical_storms += 1
            tropical_cyclones += f"{await hurricane_generator.classify(mph, location)} {name}, with {mph} mph winds ({kph} kph winds)\n"
            if mph > 74:
                hurricanes += 1
            if mph > 110:
                major_hurricanes += 1
        stats = str(f"Depressions: {tropical_depressions}\n"
                    f"Storms: {tropical_storms}\n"
                    f"Hurricanes: {hurricanes}\n"
                    f"Major Hurricanes: {major_hurricanes}\n")
        embed = embeds.twoembed(f"{str(year).replace('None', str(list_of_years[0]))} {location} Hurricane Season",
                                tropical_cyclones)
        embed.add_field(name="Statistics", value=stats, inline=True)
        try:
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            pasteurl = await self.mystbin.post(
                f"**__{str(year).replace('None', str(list_of_years[0]))} {location} Hurricane Season__**\n\n\n"
                f"{tropical_cyclones}\n\n\n"
                f"``Statistics```\n"
                f"**__{stats}__**", syntax="markdown")
            embed = embeds.twoembed(
                f"{str(year).replace('None', str(list_of_years[0]))} {location} Hurricane Season",
                f"Output was too long so I put it on [mystb.in.](https://mystb.in/)\n"
                f"Check it out [**here!**]({pasteurl})")
            embed.add_field(name="Statistics", value=stats, inline=True)
            await ctx.send(embed=embed)

    @generateseason.error
    async def generateseason_error(self, ctx, error):
        await ctx.message.add_reaction("<:compass_bot_no:809974728915419177>")
        if isinstance(error, discord.errors.HTTPException):
            return

    @commands.group(help="The Compass bot's poll command. You can use poll classic or poll number 1-10.")
    async def poll(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=embeds.twoembed(f"The two sub commands for poll are;",
                                                 f"{ctx.prefix}poll classic or {ctx.prefix}poll number [1-10]!"))

    @poll.command(help="The original poll command.")
    async def classic(self, ctx, *, question: str = None):
        if question is None:
            question = "N/A"
        embed = embeds.mainembed(f"Question asked by {ctx.message.author}!", f"{question}",
                                 "<:green_square:779529584201695272> = Yes"
                                 "\n<:yellow_square:779529584201695272> = Neutral"
                                 "\n<:red_square:779529584201695272> = No"
                                 "\n<:purple_square:779530441450848277> = Other"
                                 "\n<:grey_question:779529584201695272> = Maybe")
        embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
        msg = await ctx.send(embed=embed)
        await useful_functions.poll_classic(msg)

    @poll.command(help="A number poll. You can specify a number from 1-10 but it is not required.", name="number")
    async def number(self, ctx, num: typing.Optional[int] = None):
        await useful_functions.number_poll(ctx.message, num)

    @commands.command(help="Ships the author and a specified user (you don't have to provide a user.)")
    async def ship(self, ctx, *, user: typing.Union[discord.Member, discord.User] = None):
        if user is ctx.author:
            raise commands.BadArgument("You can't ship yourself with yourself.")
        elif user is None:
            user = random.choice(list(not m.bot for m in ctx.guild.members))
        else:
            number = random.randint(0, 100)
            desc = await useful_functions.ship(number)
        embed = embeds.mainembed(f"{ctx.author}'s chances with {user}!", f"{number}%", desc)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Posts the tab list of 2b2t.")
    async def tablist(self, ctx):
        embed = embeds.imgembed("Your tablist!",
                                "https://tab.2b2t.dev/")
        await ctx.send(embed=embed)

    @commands.command(help="Posts yours or a other user's dick size.")
    async def dicksize(self, ctx, *, user: discord.User = None):
        number = random.randint(0, 20)
        member = ""
        your_or_yours = ""
        centimeters = number + 2
        inches = round(centimeters / 2.54)
        feet = round(inches / 12)
        measurements = ""
        if user is None:
            member += str(ctx.message.author)
            your_or_yours += ", your"
        else:
            member += str(user)
            your_or_yours += "'s"
        if feet < 1:
            measurements += f"{centimeters} cm, {inches} inches"
        if feet > 1:
            measurements += f"{centimeters} cm, {inches} inches/{feet} feet"
        else:
            await ctx.send(embed=embeds.twoembed(f"{member}{your_or_yours} dick size is...",
                                                     f"8{str('=') * number}D ({measurements})"))

    @commands.command(help="Flips a coin.")
    async def coinflip(self, ctx):
        coin = random.choice(["Heads!", "Tails!"])
        await ctx.send(embed=embeds.twoembed(coin,
                                             "🪙"))

    @commands.command(help="Plays a game of rock paper scissors.", aliases=['rps'])
    async def rockpaperscissors(self, ctx):
        timeoutbed = embeds.twoembed("Timed out.",
                                     "you spent too long lol")
        await ctx.send(embed=embeds.twoembed("Rock Paper Scissors menu",
                                             "**1** - Play against the AI.\n"
                                             "~~**2** - Play against another person.~~ non-existent for now"))
        try:
            moment = await self.bot.wait_for('message', timeout=180, check=lambda msg:
            (msg.author.id == ctx.author.id and msg.channel == ctx.channel))
        except asyncio.TimeoutError:
            await ctx.send(embed=timeoutbed)
            return
        else:
            if moment.content.lower()[0] == '1':
                ai_move = random.choice(["Rock", "Paper", "Scissors"])
                await ctx.send(embed=embeds.twoembed("I've cast my move! Now you cast yours.",
                                                     "**1** - Rock\n"
                                                     "**2** - Paper\n"
                                                     "**3** - Scissors"))
                try:
                    bruh_moment = await self.bot.wait_for('message', timeout=180, check=lambda msg:
                    (msg.author.id == ctx.author.id and msg.channel == ctx.channel))
                except asyncio.TimeoutError:
                    await ctx.send(embed=timeoutbed)
                    return
                else:
                    human_move = str(bruh_moment.content.lower()[0]).replace("1", "Rock").replace("2", "Paper").replace(
                        "3", "Scissors")
                    if f"{ai_move} {human_move}" in ["Rock Paper", "Paper Scissors", "Scissors Rock"]:
                        status = "you won!"
                    elif f"{ai_move} {human_move}" in ["Paper Rock", "Scissors Paper", "Rock Scissors"]:
                        status = "you lost."
                    elif f"{ai_move} {human_move}" in ["Rock Rock", "Paper Paper", "Scissors Scissors"]:
                        status = "there was a draw, oops."
                    await ctx.send(embed=embeds.twoembed(f"{ctx.author}, {status}",
                                                         f"The AI played: {ai_move}\n"
                                                         f"You played: {human_move}"))

    @commands.command(help="Posts a random string. You can also provide a string that will be randomized if you would like.")
    async def randomstring(self, ctx, *, string: typing.Union[str] = None):
        if string is None:
            string = 'abcdefghijklmnopqrstuvwxyz1234567890'
        string_list = [str(random.choice(string)) for _ in range(random.randint(1, len(string)))]
        await ctx.send(string_list)

    async def find(self, user1, user2):
        async with aiosqlite.connect("storage.db") as connection:
            try:
                await connection.execute(f"""SELECT * FROM Notes WHERE user1 = "{user1.id}" AND user2 = "{user2.id}";""")
            except Exception:
                return False
            else:
                return True

    @commands.group(name="note", aliases=["notes"], help="The base group for adding, removing, or showing notes on a user. If you want to show a note, just type the group name followed by a user.", invoke_without_command=True)
    async def _note(self, ctx, user: checks.UserSearcher, *, note: commands.clean_content(escape_markdown=True, fix_channel_mentions=True, use_nicknames=True) = None):
        if note is None:
            async with aiosqlite.connect("storage.db") as connection:
                async with connection.execute(f"""SELECT * FROM Notes WHERE user1 = "{ctx.author.id}" AND """
                                              f"""user2 = "{user.id}";""") as cursor:
                    info = await cursor.fetchone()
                    note = info[0]
                    time = datetime.datetime.strptime(info[1], "%Y-%m-%d %H:%M:%S")
            embed = embeds.twoembed(f"Your note on {user}!",
                                    note, timestamp=False)
            embed.timestamp = time
            await ctx.send(embed=embed)
        else:
            if await self.find(ctx.author, user) is True:
                raise commands.BadArgument(f"There is a note on {user}! Delete this note before adding one.")
            else:
                time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                async with aiosqlite.connect("storage.db") as connection:
                    await connection.execute(f"""INSERT INTO Notes VALUES ("{note}", "{time}", "{ctx.author.id}", "{user.id}");""")
                    await connection.commit()
                await ctx.send("Success!")

    @_note.command(help="Edits a note.")
    async def edit(self, ctx, user: checks.UserSearcher, *, note: commands.clean_content(escape_markdown=True, fix_channel_mentions=True, use_nicknames=True)):
        if await self.find(ctx.author, user) is False:
            raise commands.BadArgument(f"There is no note on {user}! Add a note before editing.")
        else:
            async with aiosqlite.connect("storage.db") as connection:
                await connection.execute(f"""UPDATE Notes SET note = "{note}" WHERE user1 = "{ctx.author.id}" AND user2 = "{user.id}";""")
                await connection.commit()
            await ctx.send("Success!")

    @commands.command(help="Roll with added modifiers.")
    async def megaroll(self, ctx, argument: str, *, modifiers: str = None):
        argument = [int(arg) for arg in argument.split("d")]
        result = random.randint(argument[0], argument[1])
        if modifiers is not None:
            if modifiers.startswith("-"):
                modifiers.strip("-")
                calculation = result-int(modifiers)
            elif modifiers.startswith("+"):
                modifiers.strip("+")
                calculation = result + int(modifiers)
            elif modifiers.startswith("/"):
                modifiers.strip("/")
                calculation = result/int(modifiers)
            elif modifiers.startswith("*"):
                modifiers.strip("*")
                calculation = result+int(modifiers)
            await ctx.send(f"{calculation} (Originally {result})")
        else:
            await ctx.send(result)

    @commands.command(help="Posts an image of a compass.")
    async def compass(self, ctx):
        compass = random.choice(useful_functions.compasses)
        embed = embeds.imgembed("Your Compass!", compass)
        embed.url = compass
        await ctx.send(embed=embed)

    @commands.command(help="Posts a random country.", aliases=["rcountry", "randcountry"])
    async def randomcountry(self, ctx):
        country = random.choice(list(pycountry.countries)).__dict__["_fields"]
        embed = discord.Embed(color=self.bot.base_color, title=f"Your random country is {country['name']}!")
        [embed.add_field(name=field.title().replace("_", " "), value=country[field]) for field in country]
        embed.set_thumbnail(url=f"https://flagpedia.net/data/flags/w580/{country['alpha_2'].lower()}.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
