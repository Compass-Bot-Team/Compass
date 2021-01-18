import discord
import random
import wikipedia
import datetime
import objectfile
import asyncio
import yaml
import mystbin
import typing
import gtts
import io
from databases import asqlite
from discord.ext import commands, menus

ymlconfig = yaml.safe_load(open('config.yml'))
mystbin_client = mystbin.Client()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def tts_moment(self, text):
        ret = io.BytesIO()
        speech = gtts.gTTS(text)
        speech.write_to_fp(ret)
        ret.seek(0)
        return ret

    @commands.command()
    async def tts(self, ctx, *, text: typing.Union[str, commands.clean_content]):
        try:
            fp = await ctx.bot.loop.run_in_executor(None, self.tts_moment, text)
            await ctx.send(file=discord.File(fp, filename="tts.mp3"))
        except Exception:
            await ctx.send(embed=objectfile.newfailembed("This text has no letters or numbers!",
                                                         "pls fix"))

    @commands.command()
    async def say(self, ctx, *, what_to_be_said=None):
        author = ctx.message.author
        author_avatar = ctx.message.author.avatar_url
        current_time = ctx.message.created_at
        if what_to_be_said is None:
            msg = f"{author} said nothing!"
        else:
            msg = what_to_be_said.replace("@", "@\u200b")
        embed = discord.Embed(colour=discord.Colour.from_rgb(122, 141, 207),
                              title=f"Message sent by {author}!", description=msg)
        embed.set_thumbnail(url=author_avatar)
        embed.set_footer(text=f"{current_time}")
        await ctx.send(embed=embed)

    @commands.command()
    async def saytext(self, ctx, *, replace):
        msg = replace.replace("@", "@\u200b")
        author = ctx.message.author
        current_time = ctx.message.created_at
        await ctx.send(f"__Say command executed!__\n**Message sent by {author}**\n{msg}\n**Time**\n{current_time}")

    @commands.command()
    async def quote(self, ctx):
        openfile = open("databases/quotes.txt", "r").readlines()
        file = random.choice(openfile).split("|")
        embed = objectfile.twoembed("Your quote!",
                                    str(f"> {file[0]}"))
        embed.set_footer(text=str(f"- {file[1]}"))
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        async with asqlite.connect('databases/memes.db') as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM Memes ORDER BY RANDOM() LIMIT 1;")
                fetchraw = c.fetchone()
                fetchcalc = str(fetchraw).replace("('", "").replace(")", "").replace("%27,", "").replace("',", "")
                await ctx.send(f"Your meme!\n{fetchcalc}")
                await conn.close()

    @commands.command()
    async def wikipedia(self, ctx, *, arg):
        wikipedia.set_lang("en")
        query = arg
        search_results = wikipedia.page(query)
        if query == "":
            wikipediapage = wikipedia.page("Wikipedia")
            embed = objectfile.twoembed(wikipediapage.title,
                                        wikipedia.summary(wikipediapage, sentences=2))
            embed.set_footer(text=wikipediapage.url)
            await ctx.send(embed=embed)
        else:
            embed = objectfile.twoembed(search_results.title,
                                        wikipedia.summary(query, sentences=2))
            embed.set_footer(text=search_results.url)
            await ctx.send(embed=embed)

    @commands.command()
    async def someone(self, ctx):
        await ctx.send(embed=objectfile.twoembed(f"{ctx.message.author}, here's someone.",
                                                 str(random.choice(ctx.message.guild.members))))

    @commands.command(name='8ball')
    async def _8ball(self, ctx):
        current_time = ctx.message.created_at
        async with asqlite.connect('databases/8ballresponses.db') as conn:
            async with conn.cursor() as c:
                await c.execute("SELECT * FROM 8ballresponses ORDER BY RANDOM() LIMIT 1;")
                fetch = await c.fetchone()
                responses = str(fetch)
                embed = objectfile.twoembed(str(responses),
                                            f"I don't know if this is a good or bad thing.")
                embed.set_footer(text=f"{current_time}")
                await ctx.send(embed=embed)
                await conn.close()

    @commands.command(pass_context=True, name='eat')
    async def eat(self, ctx):
        current_time = ctx.message.created_at
        async with asqlite.connect('databases/8ballresponses.db') as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM eatresponses ORDER BY RANDOM() LIMIT 1;")
                fetchraw = c.fetchone()
                fetchcalc = str(fetchraw).replace("('", "").replace(")", "").replace("%27,", "").replace("',", "")
                await ctx.send(embed=objectfile.twoembed("Eating", "NOM"))
                async with ctx.channel.typing():
                    await asyncio.sleep(5)
                    embed = objectfile.twoembed(fetchcalc,
                                                "NOM")
                    embed.set_footer(text=f"{current_time}")
                    await ctx.send(embed=embed)
                await db.close()

    @commands.command()
    async def screenshot(self, ctx, url):
        if url == "https://www.pornhub.com" or "https://www.xvideos.com":
            # if ctx.message.channel.is_nsfw():
            #    await ctx.send("This could take a bit, so be patient.")
            #    embed = objectfile.twoembed("Website screenshotted!", url)
            #    embed.set_image(url=f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}")
            #    await ctx.send(embed=embed)
            #    return
            # else:
            #    embed = objectfile.twoembed("No fucking way!", "This isn't a NSFW channel bud.")
            #    await ctx.send(embed=embed)
            #    return
            pass
        await ctx.send("This could take a bit, so be patient.")
        embed = objectfile.twoembed("Website screenshotted!", url)
        embed.set_image(url=f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}")
        embed.set_footer(text="Screenshots courtesy of https://image.thum.io")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roll(self, ctx, *, arg):
        roll_list = arg.split(" ")
        min_value = 1
        max_value = int(roll_list[1])
        i = int(roll_list[0])
        filetext = []
        while i > 0:
            filetext.append(int((random.randint(min_value, max_value))))
            i -= 1
        total = sum(filetext)
        await ctx.send(embed=objectfile.mainembed(f"Dice rolled!", f"{total}", f"Total Rolls; {filetext}"))
        filetext.clear()

    @commands.command()
    async def redditrating(self, ctx):
        randomize = random.randint(0, 100)
        descriptioncalc = ""
        description = ["Neckbeard.", "You're a redditor.", "You're not a redditor."]
        if randomize == 100:
            descriptioncalc += description[0]
        if randomize > 50:
            descriptioncalc += description[1]
        if randomize < 50:
            descriptioncalc += description[2]
        await ctx.send(embed=objectfile.mainembed(f"Your redditor percentage!", randomize,
                                                  descriptioncalc))

    @commands.command()
    async def time(self, ctx):
        await ctx.send(embed=objectfile.twoembed("The current time is...", datetime.datetime.now()))

    @commands.command()
    async def tablist(self, ctx):
        embed = objectfile.twoembed("Your tablist!",
                                    "Tablist from https://tab.2b2t.dev.")
        embed.set_image(url="https://tab.2b2t.dev/")
        await ctx.send(embed=embed)

    @commands.command()
    async def embed(self, ctx):
        await ctx.send("Please provide a colo(u)r in rgb pls\n"
                       "Example: 1 1 1")
        try:
            moment0 = await self.bot.wait_for('message', timeout=180, check=lambda msg:
            (msg.author.id == ctx.author.id and msg.channel == ctx.channel))
        except asyncio.TimeoutError:
            return
        else:
            color = discord.Colour.from_rgb(int(moment0.content.lower()[0]))
        await ctx.send("What do you want the title to be?")
        try:
            bruh_moment = await self.bot.wait_for('message', timeout=180, check=lambda msg:
            (msg.author.id == ctx.author.id and msg.channel == ctx.channel))
        except asyncio.TimeoutError:
            return
        else:
            title = f"{bruh_moment.content.lower()[0]}"
        await ctx.send("What do you want the description to be?")
        try:
            bruh_moment = await self.bot.wait_for('message', timeout=180, check=lambda msg:
            (msg.author.id == ctx.author.id and msg.channel == ctx.channel))
        except asyncio.TimeoutError:
            return
        else:
            description = f"{bruh_moment.content.lower()[0]}"
        await ctx.send(discord.Embed(title=title, description=description, color=color, timestamp=datetime.datetime.utcnow()))

    @commands.command()
    async def dicksize(self, ctx, user: discord.User = None):
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
            await ctx.send(embed=objectfile.twoembed(f"{member}{your_or_yours} dick size is...",
                                                     f"8{str('=') * number}D ({measurements})"))

    @commands.cooldown(1, 5)
    @commands.command()
    async def mystbin(self, ctx, *, paste):
        await ctx.send(embed=objectfile.twoembed("Pasting to mystb.in...",
                                                 "You'll see it soon."))
        pasteurl = await mystbin_client.post(paste, syntax="python")
        await ctx.send(embed=objectfile.twoembed("Your mystb.in!",
                                                 str(pasteurl)))

    @commands.command()
    async def ship(self, ctx, user1: typing.Union[discord.Member, discord.User] = None):
        if user1 is None:
            funny_list = []
            for m in ctx.guild.members:
                if m is not m.bot:
                    funny_list.append(m)
            member = random.choice(funny_list)
        else:
            member = user1
            if member.bot:
                embed = objectfile.mainembed(f"{ctx.author}'s chances with {member}!",
                                             f"100%",
                                             f"Robot sex toys ARE BASED.")
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
                return
        if member is ctx.author:
            embed = objectfile.mainembed(f"{ctx.author}'s chances with {member}!",
                                         f"100%",
                                         f"Fucking yourself is enjoyable.")
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
            return
        else:
            number = random.randint(0, 100)
            desc = await objectfile.ship(number)
            embed = objectfile.mainembed(f"{ctx.author}'s chances with {member}!",
                                         f"{number}%",
                                         desc)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx):
        coin = random.choice(["Heads!", "Tails!"])
        await ctx.send(embed=objectfile.twoembed(coin,
                                                 "🪙"))

    @commands.command(aliases=['rps', 'rock_paper_scissors'])
    async def rockpaperscissors(self, ctx):
        timeoutbed = objectfile.twoembed("Timed out.",
                                         "you spent too long lol")
        await ctx.send(embed=objectfile.twoembed("Rock Paper Scissors menu",
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
                await ctx.send(embed=objectfile.twoembed("I've cast my move! Now you cast yours.",
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
                    if f"{ai_move} {human_move}" in ["Paper Rock", "Scissors Paper", "Rock Scissors"]:
                        status = "you lost."
                    if f"{ai_move} {human_move}" in ["Rock Rock", "Paper Paper", "Scissors Scissors"]:
                        status = "there was a draw, oops."
                    await ctx.send(embed=objectfile.twoembed(f"{ctx.author}, {status}",
                                                             f"The AI played: {ai_move}\n"
                                                             f"You played: {human_move}"))

    # @commands.command()
    # async def war(self, ctx, user: typing.Union[discord.Member, discord.User] = None):
    # if user is None:
    #    funny_list = [not m.bot for m in ctx.guild.members]
    #    member = random.choice(funny_list)
    # else:
    #    member = user
    # author_xp = 100
    # member_xp = 100
    # embed = discord.Embed(title=f"War between {ctx.author} and {member}!")
    # embed.add_field(name=)

    async def classify(self, mph):
        global classification
        if mph > 39:
            classification = "Tropical Storm"
        if mph > 74:
            classification = "Hurricane"
        if mph > 110:
            classification = "Major Hurricane"
        return classification

    @commands.command(aliases=['generate_season'])
    async def generateseason(self, ctx):
        global hurricane_amount
        global acceptable
        hurricane_list_combined = objectfile.twentytwentyhurricanelist + objectfile.greekhurricanelist
        hurricane_num = 0
        la_nina_or_el_nino = random.choice(['La Nina', 'El Nino'])
        chance = random.randint(1, 100)
        acceptable = await objectfile.acceptable(chance)
        if la_nina_or_el_nino == 'La Nina':
            hurricane_amount = random.randint(5, 37)
        if la_nina_or_el_nino == 'El Nino':
            hurricane_amount = random.randint(2, 13)
        hurricane_list_one = ""
        hurricane_list_two = ""
        hurricane_list_three = ""
        hurricane_list_four = ""
        pages = 0
        page_list = []
        for _ in range(hurricane_amount):
            mph = random.choice(acceptable)
            kph = round(mph / 1.151)
            if 0 <= hurricane_num <= 10:
                hurricane_list_one += f"{await self.classify(mph)} {hurricane_list_combined[hurricane_num]}, with {mph} mph winds ({kph} kph winds)\n"
            if 10 <= hurricane_num <= 20:
                hurricane_list_two += f"{await self.classify(mph)} {hurricane_list_combined[hurricane_num]}, with {mph} mph winds ({kph} kph winds)\n"
            if 20 <= hurricane_num <= 30:
                hurricane_list_three += f"{await self.classify(mph)} {hurricane_list_combined[hurricane_num]}, with {mph} mph winds ({kph} kph winds)\n"
            if 30 <= hurricane_num <= 40:
                hurricane_list_four += f"{await self.classify(mph)} {hurricane_list_combined[hurricane_num]}, with {mph} mph winds ({kph} kph winds)\n"
            hurricane_num += 1
        if hurricane_num < 0:
            page_list.append(objectfile.twoembed("2020 generated Hurricane season",
                                                 hurricane_list_one))
        if hurricane_num < 10:
            page_list.append(objectfile.twoembed("2020 generated Hurricane season",
                                                 hurricane_list_two))
        if hurricane_num < 20:
            page_list.append(objectfile.twoembed("2020 generated Hurricane season",
                                                 hurricane_list_three))
        if hurricane_num < 30:
            page_list.append(objectfile.twoembed("2020 generated Hurricane season",
                                                 hurricane_list_four))
        await ctx.send(embed=page_list[pages])
        #emote_list = ['\U00002b05\U0000fe0f', '\U000027a1\U000027a1', '\U0001f1fd']
        #await send.add_reaction('\U00002b05\U0000fe0f')
        #await send.add_reaction['\U000027a1\U000027a1']
        #await send.add_reaction['\U0001f1fd']

def setup(bot):
    bot.add_cog(Fun(bot))
