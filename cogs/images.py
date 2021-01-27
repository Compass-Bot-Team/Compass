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
import aiohttp
import aiofiles
import yaml
import sr_api
import typing
import random
from io import BytesIO
from functools import partial
from PIL import Image, ImageFilter
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))
client = sr_api.Client(config['srakey'])

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def blur_processor():
        img = Image.open("image.png")
        img.filter(ImageFilter.GaussianBlur()).save("image.png")

    @commands.command()
    async def blur(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                await ctx.message.attachments[0].save("image.png")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as urlgrabber:
                    file = await aiofiles.open('image.png', mode='wb')
                    await file.write(await urlgrabber.read())
                    await file.close()
        file = discord.File("image.png")
        await self.bot.loop.run_in_executor(None, partial(self.blur_processor))
        embed = objectfile.twoembed(f"{ctx.message.author}, image blurred!", "Blurry.")
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed, file=file)

    @staticmethod
    def rotate_processor(degree):
        img = Image.open("image.png")
        img.rotate(int(degree)).save("image.png")

    @commands.command()
    async def rotate(self, ctx, degree=None, url=None):
        if degree is None:
            await ctx.send(embed=objectfile.twoembed("How am I gonna rotate this?",
                                                     "I don't have a degree!\n"
                                                     "Example: compass!rotate 90 https://cdn.discordapp.com/attachments/777248921205866546/792456542640668732/compass.png"))
            return
        else:
            if url is None:
                if ctx.message.attachments[0] is not None:
                    await ctx.message.attachments[0].save("image.png")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as urlgrabber:
                        file = await aiofiles.open('image.png', mode='wb')
                        await file.write(await urlgrabber.read())
                        await file.close()
            await self.bot.loop.run_in_executor(None, partial(self.rotate_processor(degree)))
            file = discord.File("image.png")
            embed = objectfile.twoembed(f"{ctx.message.author}, image rotated!", "Rotated.")
            embed.set_image(url="attachment://image.png")
            await ctx.send(embed=embed, file=file)

    @staticmethod
    def enlarge_processor():
        img = Image.open("image.png")
        width, height = img.size
        img.resize((round(width * 1.25), round(height * 1.25))).save("image.png")

    @commands.command()
    async def enlarge(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                await ctx.message.attachments[0].save("image.png")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as urlgrabber:
                    file = await aiofiles.open('image.png', mode='wb')
                    await file.write(await urlgrabber.read())
                    await file.close()
        await self.bot.loop.run_in_executor(None, partial(self.enlarge_processor))
        file = discord.File("image.png")
        embed = objectfile.twoembed(f"{ctx.message.author}, image enlarged!", "Enlarged by 25%.")
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def gay(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        gayifier = client.filter(option="gay", url=url)
        embed = objectfile.twoembed("Your gay image!",
                                    f"[URL]({gayifier})")
        embed.set_image(url=gayifier.url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5)
    @commands.command()
    async def triggered(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        triggerfier = client.filter(option="triggered", url=url)
        embed = objectfile.twoembed("Your image/GIF just got triggered!",
                                    f"[URL]({triggerfier})")
        buffer = BytesIO(await triggerfier.read())
        file = discord.File(fp=buffer, filename="triggered.gif")
        embed.set_image(url=f"attachment://triggered.gif")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def spin(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        spinner = client.filter(option="spin", url=url)
        embed = objectfile.twoembed("Your image/GIF just got spun!",
                                    f"[URL]({spinner})")
        buffer = BytesIO(await spinner.read())
        file = discord.File(fp=buffer, filename="spun.gif")
        embed.set_image(url=f"attachment://spun.gif")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def red(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        redifier = client.filter(option="red", url=url)
        embed = objectfile.twoembed("Your image just turned to red!",
                                    f"[URL]({redifier})")
        buffer = BytesIO(await redifier.read())
        file = discord.File(fp=buffer, filename="red.png")
        embed.set_image(url=f"attachment://red.png")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def green(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        greenifier = client.filter(option="green", url=url)
        embed = objectfile.twoembed("Your image just turned to green!",
                                    f"[URL]({greenifier})")
        buffer = BytesIO(await greenifier.read())
        file = discord.File(fp=buffer, filename="green.png")
        embed.set_image(url=f"attachment://green.png")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def blue(self, ctx, url=None):
        if url is None:
            if ctx.message.attachments[0] is not None:
                url = ctx.message.attachments[0].url
        blueifier = client.filter(option="blue", url=url)
        embed = objectfile.twoembed("Your image just turned to blue!",
                                    f"[URL]({blueifier})")
        buffer = BytesIO(await blueifier.read())
        file = discord.File(fp=buffer, filename="blue.png")
        embed.set_image(url=f"attachment://blue.png")
        await ctx.send(embed=embed, file=file)

    @commands.cooldown(1, 5)
    @commands.command()
    async def amongus(self, ctx, user: typing.Union[discord.User, discord.Member] = None):
        if user is None:
            member = ctx.author
        else:
            member = user
        among = client.amongus(username=str(member.display_name), avatar=str(member.avatar_url), impostor=random.choice(
            [False, True]))
        buffer = BytesIO(await among.read())
        file = discord.File(fp=buffer, filename="amongus.gif")
        embed = objectfile.twoembed(f"{user} was ejected!",
                                    f"[URL]({among})")
        embed.set_image(url=f"attachment://amongus.gif")
        await ctx.send(embed=embed, file=file)


def setup(bot):
    bot.add_cog(Images(bot))
