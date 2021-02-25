import aiohttp
import base64
import json
import discord
import datetime
import pytz
from cogs.error_handling import error_handle
from utils import embeds
from discord.ext import commands


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Posts the minecraft skin of a given username.")
    async def skin(self, ctx, *, user: str):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{user}") as api:
                    jsonified = await api.json()
                    if "error" in jsonified:
                        raise commands.BadArgument("User not found.")
                async with session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{jsonified['id']}") as api_again:
                    jsonified_again = json.loads(base64.b64decode((await api_again.json())["properties"][0]["value"]))
        await ctx.send(embed=embeds.imgembed(f"{user}'s skin!", jsonified_again["textures"]["SKIN"]["url"]))

    @skin.error
    async def skin_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(embed=embeds.imgembed("Status code 204!", "https://http.cat/204"))
        else:
            return await error_handle()

    @commands.group(help='Posts the stats of [2b2t.](https://en.wikipedia.org/wiki/2b2t)', name="2b2t",
                    invoke_without_command=True)
    async def _2b2t(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://2b2t.io/api/queue", params={"last": "true"}) as queue:
                    queue_info = int((await queue.json())[0][1])
                async with session.get("https://api.2b2t.dev/prioq") as priorityqueueapi:
                    jsonified = await priorityqueueapi.json()
                    priority = int(jsonified[1])
            embed = discord.Embed(title="2b2t stats!", color=self.bot.base_color)
            embed.add_field(name="Queue length", value=f"All: {queue_info+priority:,}\n"
                                                       f"Priority: {priority:,}\n"
                                                       f"Normal: {queue_info:,}")
        await ctx.send(embed=embed)

    async def time_converter(self, strtime):
        return (datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.timezone("US/Eastern"))
                ).astimezone(pytz.utc)

    @_2b2t.command(help='Shows stats of a 2b2t user.')
    async def user(self, ctx, *, username: str):
        params_1 = {"username": username}
        params_2 = {"lastdeath": username}
        params_3 = {"lastkill": username}
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.2b2t.dev/stats", params=params_1) as api_1:
                    if len(await api_1.json()) == 0:
                        raise commands.BadArgument("User not found.")
                    else:
                        jsonified_1 = (await api_1.json())[0]
                async with session.get("https://api.2b2t.dev/stats", params=params_2) as api_2:
                    if len(await api_2.json()) == 0:
                        jsonified_2 = None
                    else:
                        jsonified_2 = (await api_2.json())[0]
                async with session.get("https://api.2b2t.dev/stats", params=params_3) as api_3:
                    if len(await api_3.json()) == 0:
                        jsonified_3 = None
                    else:
                        jsonified_3 = (await api_3.json())[0]
        embed = discord.Embed(title=f"{username}'s 2b2t stats!", color=self.bot.base_color,
                              timestamp=datetime.datetime.utcnow(), url="https://2b2t.dev")
        if jsonified_2 is not None:
            last_death_time = await self.time_converter(f"{jsonified_2['date']} {jsonified_2['time']}")
            embed.add_field(name="Last Death (UTC)", value=f"{last_death_time}\n{jsonified_2['message']}", inline=False)
        if jsonified_3 is not None:
            last_kill_time = await self.time_converter(f"{jsonified_3['date']} {jsonified_3['time']}")
            embed.add_field(name="Last Kill (UTC)", value=f"{last_kill_time}\n{jsonified_3['message']}", inline=False)
        embed.add_field(name="Total Kills", value=f"{jsonified_1['kills']:,}", inline=True)
        embed.add_field(name="Total Deaths", value=f"{jsonified_1['deaths']:,}", inline=True)
        embed.add_field(name="Total Joins", value=f"{jsonified_1['joins']:,}", inline=True)
        embed.add_field(name="Total Leaves", value=f"{jsonified_1['leaves']:,}", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Minecraft(bot))
