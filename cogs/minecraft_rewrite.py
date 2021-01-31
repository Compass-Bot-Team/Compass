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
import aiohttp
import asyncpixel
import aio2b2t
import objectfile
import asyncio
import yaml
import typing
import io
import aiosqlite
from MojangAPI import Client
from datetime import datetime
from discord.ext import commands, tasks

config = yaml.safe_load(open('config.yml'))
client = asyncpixel.Client(config['hypixelapikey'])

async def iourl(endpoint):
    return f"https://2b2t.io/api/{endpoint}"

async def devurl(endpoint):
    return f"https://api.2b2t.dev/{endpoint}"

class Minecraft(commands.Cog, name='Minecraft (Being Rewritten)'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def minecraft(self, ctx, *, server: str):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://eu.mc-api.net/v3/server/ping/{server}') as x:
                    api = await x.json()
        if 'error' in api:
            return await ctx.send(embed=objectfile.newfailembed(f"No Minecraft server IP matching: {server}!",
                                                                f"Try something else."))
        embed = discord.Embed(colour=0x202225, title=f"{server}'s stats!", description=f"Total Players: {api['players']['online']}/{api['players']['max']}")
        embed.add_field(name="Version", value=api['version']['name'])
        embed.set_thumbnail(url=str(api['favicon']))
        embed.add_field(name="Online", value=str(api['online']).title())
        await ctx.send(embed=embed)

    @minecraft.command()
    async def skin(self, ctx, username: str):
        async with ctx.channel.typing():
            user = await Client.User.createUser(username)
            profile = await user.getProfile()
        await ctx.send(embed=objectfile.imgembed(f"{username}'s Minecraft skin!", profile.skin))

    @commands.group(name='2b2t', invoke_without_command=True)
    async def _2b2t(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(await iourl("queue?last=true")) as o:
                    api1 = list(await o.json())[0]
                async with cs.get(await devurl("status")) as p:
                    api2 = list(await p.json())[0]
                async with cs.get(await devurl("prioq")) as q:
                    api3 = list(await q.json())
        totalqueue = int(api1[1]) + int(api3[1])
        embed = discord.Embed(colour=0x202225, title=f"2b2t stats!")
        embed.add_field(name="Total Queue", value=str(totalqueue))
        embed.add_field(name="Uptime", value=api2[3])
        embed.add_field(name="TPS", value=api2[0])
        await ctx.send(embed=embed)

    @_2b2t.command(aliases=['user_stats'])
    async def userstats(self, ctx, user: str):
        global name
        name = user
        async with ctx.channel.typing():
            userstats = aio2b2t.userstats()
        embed = discord.Embed(colour=0x202225, title=f"{user}'s stats!", description=f"Admin Level: {await userstats.adminlevel(user)}/1, "
                                                                                     f"UUID: {await userstats.uuid(user)}", url=aio2b2t_page)
        kills = await userstats.kills(user)
        deaths = await userstats.deaths(user)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Kill to Death Ratio", value=int(kills)/int(deaths), inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="Joins", value=await userstats.joins(user), inline=True)
        embed.add_field(name="Leaves", value=await userstats.leaves(user), inline=True)
        embed.add_field(name="DB ID", value=await userstats.id(user), inline=True)
        await ctx.send(embed=embed)

    @userstats.error
    async def userstats_error(self, ctx, error):
        return await ctx.send(embed=objectfile.newfailembed(f"No user going by {name}.",
                                                            "Try searching somebody else."))

    @_2b2t.command(aliases=['last_death'])
    async def lastdeath(self, ctx, user: str):
        global name1
        name1 = user
        async with ctx.channel.typing():
            lastdeath = aio2b2t.lastdeath()
        embed = discord.Embed(colour=0x202225, title=f"{user}'s last death!", url=aio2b2t_page)
        embed.add_field(name="Message", value=await lastdeath.message(user), inline=True)
        embed.add_field(name="Time", value=await lastdeath.datetime(user), inline=True)
        embed.add_field(name="DB ID", value=await lastdeath.id(user), inline=True)
        await ctx.send(embed=embed)

    @lastdeath.error
    async def lastdeath_error(self, ctx, error):
        return await ctx.send(embed=objectfile.newfailembed(f"No user going by {name1}.",
                                                            "Try searching somebody else."))

    @_2b2t.command(aliases=['last_kill'])
    async def lastkill(self, ctx, user: str):
        global name2
        name2 = user
        async with ctx.channel.typing():
            lastkill = aio2b2t.lastkill()
        embed = discord.Embed(colour=0x202225, title=f"{user}'s last kill!", url=aio2b2t_page)
        embed.add_field(name="Message", value=await lastkill.message(user), inline=True)
        embed.add_field(name="Time", value=await lastkill.datetime(user), inline=True)
        embed.add_field(name="DB ID", value=await lastkill.id(user), inline=True)
        await ctx.send(embed=embed)

    @lastkill.error
    async def lastkill_error(self, ctx, error):
        return await ctx.send(embed=objectfile.newfailembed(f"No user going by {name2}.",
                                                            "Try searching somebody else."))


def setup(bot):
    bot.add_cog(Minecraft(bot))
