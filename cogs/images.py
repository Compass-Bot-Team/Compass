# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import aiozaneapi
import discord
import io
import validators
import typing
import sr_api
import aiohttp
from functools import partial
from utils import embeds, image_processors
from discord.ext import commands


class Images(commands.Cog, description='The bucket load of image manipulation.'):
    def __init__(self, bot):
        self.bot = bot
        self.client = aiozaneapi.Client(self.bot.config["zanekey"])
        self.sr_client = sr_api.Client()

    async def none(self, ctx):
        if ctx.message.attachments:
            argument = str(ctx.message.attachments[0].url)
        else:
            argument = str(ctx.author.avatar_url)
        return argument

    async def none_srapi(self, ctx):
        if ctx.message.attachments:
            argument = str(ctx.message.attachments[0].url).replace(".webp", ".png").replace(".gif", ".png")
        else:
            argument = str(ctx.author.avatar_url_as(format="png", static_format="png"))
        return argument

    async def convert_to_bytes_better(self, user, argument, ctx):
        if user is not None and argument is None:
            bytes_to_give = bytes(await user.avatar_url.read())
        elif argument is None:
            if ctx.message.attachments:
                bytes_to_give = bytes(await ctx.message.attachments[0].read())
            else:
                bytes_to_give = bytes(await ctx.author.avatar_url.read())
        elif argument is not None:
            async with aiohttp.ClientSession() as session:
                async with session.get(argument) as grabber:
                    bytes_to_give = bytes(await grabber.read())
        return bytes_to_give

    @commands.command(help='Blurs an image, URL or user.')
    async def blur(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        async with ctx.channel.typing():
            bytes_to_give = await self.convert_to_bytes_better(user, argument, ctx)
            buy_one_and_get_one_free = await self.bot.loop.run_in_executor(None, partial(image_processors.blur_processor, bytes_to_give))
        file = discord.File(filename="blur.png", fp=buy_one_and_get_one_free)
        embed = embeds.imgembed("Blurred!", "attachment://blur.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(help='Rotates an image, URL or user.')
    async def rotate(self, ctx, degree: int, user: typing.Optional[discord.User], *, argument: str = None):
        async with ctx.channel.typing():
            bytes_to_give = await self.convert_to_bytes_better(user, argument, ctx)
            buy_one_and_get_one_free = await self.bot.loop.run_in_executor(None, partial(
                image_processors.rotate_processor, degree, bytes_to_give))
        file = discord.File(filename="rotate.png", fp=buy_one_and_get_one_free)
        embed = embeds.imgembed("Rotated!", "attachment://rotate.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(help='Enlarges an image, URL or user.')
    async def enlarge(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        async with ctx.channel.typing():
            bytes_to_give = await self.convert_to_bytes_better(user, argument, ctx)
            buy_one_and_get_one_free = await self.bot.loop.run_in_executor(None, partial(
                image_processors.enlarge_processor, bytes_to_give))
        file = discord.File(filename="enlarged.png", fp=buy_one_and_get_one_free)
        embed = embeds.imgembed("Enlarged!", "attachment://enlarged.png")
        await ctx.send(file=file, embed=embed)

    @commands.command(help='Turns an image, URL, or user into the floor.')
    async def floor(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            floor = await self.client.floor(str(argument))
        file = discord.File(fp=floor, filename="floor.gif")
        embed = embeds.imgembedforzane("Floor.",
                                       "attachment://floor.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Turns an image, URL, or user into magic.', aliases=['magik'])
    async def magic(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            magic = await self.client.magic(str(argument))
        file = discord.File(fp=magic, filename="magic.gif")
        embed = embeds.imgembedforzane("Magic.",
                                       "attachment://magic.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Deepfries an image, URL, or user.')
    async def deepfry(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            deepfry = await self.client.deepfry(str(argument))
        file = discord.File(fp=deepfry, filename="deepfry.png")
        embed = embeds.imgembedforzane("Deepfried.",
                                       "attachment://deepfry.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Turns an Image, URL or User into dots.')
    async def dots(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            dots = await self.client.dots(str(argument))
        file = discord.File(fp=dots, filename="dots.png")
        embed = embeds.imgembedforzane("Dots.",
                                       "attachment://dots.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Converts an Image, URL or User into a JPEG.')
    async def jpeg(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            jpeg = await self.client.jpeg(str(argument))
        file = discord.File(fp=jpeg, filename="jpeg.png")
        embed = embeds.imgembedforzane("JPEG.",
                                       "attachment://jpeg.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Spreads an Image, URL or User.')
    async def spread(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            spread = await self.client.spread(str(argument))
        file = discord.File(fp=spread, filename="spread.gif")
        embed = embeds.imgembedforzane("Spreaded.",
                                       "attachment://spread.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Turns an Image, URL or User into a Cube.')
    async def cube(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            cube = await self.client.cube(str(argument))
        file = discord.File(fp=cube, filename="cube.png")
        embed = embeds.imgembedforzane("Cube.",
                                       "attachment://cube.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(help='Sorts an Image, URL or User.')
    async def sort(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if user is not None and argument is None:
            argument = str(user.avatar_url)
        if argument is None:
            argument = await self.none(ctx)
        if validators.url(str(argument)) is False:
            return await ctx.send("Invalid URL.")
        async with ctx.channel.typing():
            sort = self.client.sort(str(argument))
        file = discord.File(fp=sort, filename="sort.png")
        embed = embeds.imgembedforzane("Sorted.",
                                       "attachment://sort.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Turns an image, gif or user gay (like the frogs)")
    async def gay(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = argument.replace(".webp", ".png").replace(".gif", ".png")
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            gayifier = self.sr_client.filter(option="gay", url=argument)
        embed = embeds.imgembedforsrapi("Gay!",
                                        "attachment://gay.gif")
        buffer = io.BytesIO(await gayifier.read())
        file = discord.File(fp=buffer, filename="gay.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Triggers an image, gif or user.")
    async def triggered(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = argument.replace(".webp", ".png").replace(".gif", ".png")
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            triggerfier = self.sr_client.filter(option="triggered", url=argument)
        embed = embeds.imgembedforsrapi("Triggered!",
                                        "attachment://triggered.gif")
        buffer = io.BytesIO(await triggerfier.read())
        file = discord.File(fp=buffer, filename="triggered.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Spins an image, gif or user.")
    async def spin(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = str(argument.replace(".webp", ".png").replace(".gif", ".png"))
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            spinner = self.sr_client.filter(option="spin", url=argument)
        embed = embeds.imgembedforsrapi("Spinning!",
                                        "attachment://spun.gif")
        buffer = io.BytesIO(await spinner.read())
        file = discord.File(fp=buffer, filename="spun.gif")
        embed.set_image(url=f"attachment://spun.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Turns an image, gif or user red.")
    async def red(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = str(argument.replace(".webp", ".png").replace(".gif", ".png"))
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            redifier = self.sr_client.filter(option="red", url=argument)
        embed = embeds.imgembedforsrapi("Red!",
                                        "attachment://red.gif")
        buffer = io.BytesIO(await redifier.read())
        file = discord.File(fp=buffer, filename="red.gif")
        embed.set_image(url=f"attachment://red.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Turns an image, gif or user green.")
    async def green(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = str(argument.replace(".webp", ".png").replace(".gif", ".png"))
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            greenifier = self.sr_client.filter(option="green", url=argument)
        embed = embeds.imgembedforsrapi("Green!",
                                        "attachment://green.gif")
        buffer = io.BytesIO(await greenifier.read())
        file = discord.File(fp=buffer, filename="green.gif")
        embed.set_image(url=f"attachment://green.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Turns an image, gif or user blue.")
    async def blue(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = str(argument.replace(".webp", ".png").replace(".gif", ".png"))
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            blueifier = self.sr_client.filter(option="blue", url=argument)
        embed = embeds.imgembedforsrapi("Blue!",
                                        "attachment://blue.gif")
        buffer = io.BytesIO(await blueifier.read())
        file = discord.File(fp=buffer, filename="blue.gif")
        embed.set_image(url=f"attachment://blue.gif")
        await ctx.send(embed=embed, file=file)

    @commands.command(help="Wastes an image, gif or user.")
    async def wasted(self, ctx, user: typing.Optional[discord.User], *, argument: str = None):
        if argument is not None:
            argument = str(argument.replace(".webp", ".png").replace(".gif", ".png"))
        if user is not None and argument is None:
            argument = str(user.avatar_url_as(format="png", static_format="png"))
        if argument is None:
            argument = str(await self.none_srapi(ctx))
        async with ctx.channel.typing():
            wastifier = self.sr_client.filter(option="wasted", url=argument)
        embed = embeds.imgembedforsrapi("Wasted!",
                                        "attachment://wasted.gif")
        buffer = io.BytesIO(await wastifier.read())
        file = discord.File(fp=buffer, filename="wasted.gif")
        embed.set_image(url=f"attachment://wasted.gif")
        await ctx.send(embed=embed, file=file)

    def cog_unload(self):
        self.task.cancel()
        session.close()


def setup(bot):
    bot.add_cog(Images(bot))
