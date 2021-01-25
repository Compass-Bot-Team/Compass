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
import sr_api
import async_cleverbot
import yaml
from bot import has_admin, blacklisted
from datetime import datetime
from discord.ext import commands
from discord.utils import get

ymlconfig = yaml.safe_load(open("config.yml"))
client = sr_api.Client()
cleverbot = async_cleverbot.Cleverbot(ymlconfig['travitiakey'])
support_server_id = 738530998001860629
checkfail = objectfile.newfailembed("You aren't in AntoLib (or you aren't admin there!)",
                                    "Try harder.")

def antolib():
    def predicate(ctx):
        return ctx.guild.id == 738530998001860629
    return commands.check(predicate)

def blacklisted_or_not():
    def predicate(ctx):
        return ctx.guild.id == 738530998001860629
    return commands.check(predicate)

class AntoLib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.guild.id != support_server_id:
            return
        if message.author.bot:
            return
        if message.channel.id == 801971149285883955:
            if len(message.content) < 3 or len(message.content) > 60:
                await message.channel.send(embed=objectfile.newfailembed("All messages must be above 3 and below 60 characters!",
                                                                         "API limitations, sowwy."))
            else:
                chatbot = await cleverbot.ask(str(message.content))
                embed = objectfile.twoembed(f"Cleverbot's response!", chatbot)
                await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.guild.id != support_server_id:
            return
        if message.author.bot:
            return
        embed = discord.Embed(title=f"Message deleted in #{message.channel}!",
                              description=f"Message from <@!{message.author.id}>",
                              color=discord.Color.from_rgb(122, 141, 207))
        embed.add_field(name="Message", value=message.content)
        embed.set_footer(text=f"{message.created_at}")
        embed.set_thumbnail(url=f"{message.author.avatar_url}")
        logchannel = self.bot.get_channel(777039726506934273)
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        author = before.author
        if not before.guild or before.guild.id != support_server_id:
            return
        if before.author.bot:
            return
        embed = discord.Embed(title=f"Message edited in #{before.channel}!",
                              description=f"Message from <@!{before.author.id}>",
                              color=discord.Color.from_rgb(122, 141, 207))
        embed.add_field(name="Message Before", value=f"{before.content}", inline=True)
        embed.add_field(name="Message After", value=f"{after.content}", inline=True)
        embed.set_footer(text=f"{datetime.now()}")
        embed.set_thumbnail(url=f"{author.avatar_url}")
        logchannel = self.bot.get_channel(777039726506934273)
        await logchannel.send(embed=embed)

    @antolib()
    @has_admin()
    @commands.command()
    async def verify(self, ctx, member: discord.Member):
        try:
            logchannel = self.bot.get_channel(777039726506934273)
            verifiedrole = get(member.guild.roles, name="Member")
            unverifiedrole = get(member.guild.roles, name="Unverified")
            if unverifiedrole in member.roles:
                await member.add_roles(verifiedrole)
                await member.remove_roles(unverifiedrole)
                embed = objectfile.successembed("User verified.",
                                                f"Verified {member}!",
                                                f"Action done by {ctx.message.author}")
                embed.set_thumbnail(url=f"{member.avatar_url}")
                await ctx.send(embed=embed)
                await logchannel.send(embed=embed)
            else:
                await ctx.send(embed=objectfile.failembed("This user is already verified.",
                                                          "Get better verification targets ffs",
                                                          f"Verified Member: {member}"))
        except commands.CheckFailure:
            await ctx.send(embed=checkfail)

    @commands.command()

def setup(bot):
    bot.add_cog(AntoLib(bot))
