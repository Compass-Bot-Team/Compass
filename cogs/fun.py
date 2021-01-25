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
import async_cleverbot
from discord.ext import commands

ymlconfig = yaml.safe_load(open('config.yml'))
mystbin_client = mystbin.Client()
cleverbot = async_cleverbot.Cleverbot(ymlconfig['travitiakey'])

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paginator = commands.Paginator()

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

    @commands.command()
    async def chat(self, ctx, *, arg:str=None):
        if arg is None:
            embed = objectfile.failembed(f"You need a message!",
                                         f"Example: {ctx.prefix}chat How's your day?",
                                         f"Try it again!")
            await ctx.send(embed=embed)
        else:
            if len(arg) < 3 or len(arg) > 60:
                await ctx.send(embed=objectfile.newfailembed("All messages must be above 3 and below 60 characters!",
                                                             "API limitations, sowwy."))
            else:
                chatbot = await cleverbot.ask(str(arg))
                embed = objectfile.twoembed(f"Cleverbot's response!", chatbot)
                await ctx.send(embed=embed)

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
            rgb = list(moment0.content.lower()[0].split(' '))
            color = discord.Colour.from_rgb(int(rgb[0]), int(rgb[1]), int(rgb[2]))
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

    @commands.command(aliases=['generate_season'])
    async def generateseason(self, ctx, year: int = None):
        global used_hurricane_list
        list_of_years = [2021, 2022, 2023, 2024, 2025, 2026]
        if year is None:
             used_hurricane_list = objectfile._2021hurricanelist
        else:
            if year == 2021:
                used_hurricane_list = objectfile._2021hurricanelist
            if year == 2022:
                used_hurricane_list = objectfile._2022hurricanelist
            if year == 2023:
                used_hurricane_list = objectfile._2023hurricanelist
            if year == 2024:
                used_hurricane_list = objectfile._2024hurricanelist
            if year == 2025:
                used_hurricane_list = objectfile._2025hurricanelist
            if year == 2026:
                used_hurricane_list = objectfile._2026hurricanelist
            if year not in list_of_years:
                return await ctx.send(embed=objectfile.newfailembed("Please provide a valid year!",
                                                                    "Valid years: 2021, 2022, 2023, 2024, 2025, 2026"))
        tropical_depression_list = objectfile.numbers
        hurricane_list_combined = used_hurricane_list + objectfile.greekhurricanelist
        tropical_depressions = 0
        tropical_storms = 0
        hurricanes = 0
        major_hurricanes = 0
        la_nina_or_el_nino = random.choice(['La Nina', 'El Nino'])
        if la_nina_or_el_nino == 'La Nina':
            hurricane_amount = random.randint(5, 37)
        if la_nina_or_el_nino == 'El Nino':
            hurricane_amount = random.randint(2, 13)
        tropical_cyclones = ""
        for _ in range(hurricane_amount):
            chance = random.randint(1, 100)
            if chance > 0:
                acceptable = [30, 35, 40, 45, 50]
            if chance > 20:
                acceptable = [35, 40, 45, 50, 60, 65]
            if chance > 30:
                acceptable = [40, 45, 50, 60, 65, 70]
            if chance > 50:
                acceptable = [45, 50, 60, 65, 70, 75]
            if chance > 60:
                acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100]
            if chance > 70:
                acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 125, 130, 140]
            if chance > 80:
                acceptable = [60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140, 145, 150, 155, 160]
            if chance > 90:
                acceptable = [80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140,
                              145, 150, 155, 160, 165, 175, 180]
            if chance > 95:
                acceptable = [90, 100, 105, 110, 115, 120, 125, 130, 140,
                              145, 150, 155, 160, 165, 175, 180, 185, 190, 195]
            mph = random.choice(acceptable)
            kph = round(mph / 1.151)
            if mph < 39:
                tropical_cyclones += (f"{await objectfile.classify(mph)} {tropical_depression_list[tropical_depressions]}, with {mph} mph winds ({kph} kph winds)\n")
                tropical_depressions += 1
            else:
                tropical_cyclones += (f"{await objectfile.classify(mph)} {hurricane_list_combined[tropical_storms]}, with {mph} mph winds ({kph} kph winds)\n")
                tropical_depressions += 1
                tropical_storms += 1
            if mph > 74:
                hurricanes += 1
            if mph > 110:
                major_hurricanes += 1
        stats = str(f"Depressions: {tropical_depressions}\n"
                    f"Storms: {tropical_storms}\n"
                    f"Hurricanes: {hurricanes}\n"
                    f"Major Hurricanes: {major_hurricanes}\n")
        embed = objectfile.twoembed(f"{str(year).replace('None', str(list_of_years[0]))} Atlantic Hurricane Season",
                                    tropical_cyclones)
        objectfile.add_field(embed, "Statistics", stats, True)
        easter_egg = random.randint(0, 100)
        if easter_egg == 100:
            objectfile.add_field(embed, "Other Systems", f"Storm Alex, with 116 mph winds ({round(116 / 1.151)} kph winds)", True)
        try:
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            pasteurl = await mystbin_client.post(f"**__{str(year).replace('None', str(list_of_years[0]))} Atlantic Hurricane Season__**\n\n\n"
                                                 f"{tropical_cyclones}\n\n\n"
                                                 f"``Statistics```\n"
                                                 f"**__{stats}__**", syntax="markdown")
            embed = objectfile.twoembed(f"{str(year).replace('None', str(list_of_years[0]))} Atlantic Hurricane Season",
                                        f"Output was too long so I put it on [mystb.in.](https://mystb.in/)\n"
                                        f"Check it out [**here!**]({pasteurl})")
            objectfile.add_field(embed, "Statistics", stats, True)
            if easter_egg == 100:
                objectfile.add_field(embed, "Other Systems",
                                     f"Storm Alex, with 116 mph winds ({round(116 / 1.151)} kph winds)", True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
