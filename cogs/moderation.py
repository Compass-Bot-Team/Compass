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
import typing
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: typing.Union[discord.Member, discord.User], reason=None):
        if ctx.author == user:
            await ctx.send(embed=objectfile.failembed(f"You can't kick yourself, {ctx.message.author}.",
                                                      "You can kick anyone BUT yourself!", "Try someone else."))
        else:
            if reason is None:
                embed = objectfile.failembed(f"Pls give a reason {ctx.message.author}.",
                                             f"This needs a reason!",
                                             f"If you don't have a reason what's the point?")
                embed.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed)
            else:
                embed1 = objectfile.failembed(f"You got kicked off {ctx.guild.name}.",
                                              f"You were kicked by {ctx.message.author}.",
                                              f"Reason; {reason}")
                embed2 = objectfile.successembed(f"User {user} kicked!", "See you later.",
                                                 "This is (probably) your last chance before a ban!")
                embed2.set_thumbnail(url=f"{user.avatar_url}")
                embed1.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed2)
                await user.send(embed=embed1)
                await user.kick()

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=objectfile.failembed("You can't kick!", "You have to get perms.", "Become monkey, "
                                                                                                   "become Discord "
                                                                                                   "mod."))
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: typing.Union[discord.Member, discord.User], reason):
        if ctx.author == user:
            await ctx.send(embed=objectfile.failembed(f"You can't ban yourself, {ctx.message.author}.",
                                                      "You can kick ban BUT yourself!", "Try someone else."))
        else:
            if reason is None:
                embed = objectfile.failembed(f"Pls give a reason {ctx.message.author}.",
                                             f"This needs a reason!",
                                             f"If you don't have a reason what's the point?")
                embed.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed)
            else:
                # Ban user
                embed1 = objectfile.failembed(f"You got banned off {ctx.guild.name}.",
                                              f"You were banned by {ctx.message.author}.",
                                              f"Reason; {reason}")
                embed1.set_thumbnail(url=f"{user.avatar_url}")
                await user.send(embed=embed1)
                embed2 = objectfile.successembed(f"User {user} banned!", "See you later.",
                                                f"Reason: {reason}")
                embed2.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed2)
                await user.ban(reason=reason, delete_message_days=0)

    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=objectfile.failembed("You can't ban!", "You have to get perms.", "Become monkey, "
                                                                                                  "become Discord "
                                                                                                  "mod."))
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, member, reason):
        user = await self.bot.get_user(member)
        if ctx.author == user:
            await ctx.send(embed=objectfile.failembed(f"You can't ban yourself, {ctx.message.author}.",
                                                      "You can kick ban BUT yourself!", "Try someone else."))
        else:
            if reason is None:
                embed = objectfile.failembed(f"Pls give a reason {ctx.message.author}.",
                                             f"This needs a reason!",
                                             f"If you don't have a reason what's the point?")
                embed.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed)
            else:
                # Ban user
                embed1 = objectfile.failembed(f"You got banned off {ctx.guild.name}.",
                                              f"You were banned by {ctx.message.author}.",
                                              f"Reason; {reason}")
                embed1.set_thumbnail(url=f"{user.avatar_url}")
                await user.send(embed=embed1)
                embed2 = objectfile.successembed(f"User {user} banned!", "See you later.",
                                                 f"Reason: {reason}")
                embed2.set_thumbnail(url=f"{user.avatar_url}")
                await ctx.send(embed=embed2)
                await user.ban(reason=reason, delete_message_days=0)

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, name):
        await self.bot.create_custom_emoji(name=str(name), image=bytes(ctx.message.attachment), roles=None,
                                           reason=None)
        await ctx.send(embed=objectfile.twoembed(f"Added emoji {name} to the server!",
                                                 "There ya go."))

    @addemoji.error
    async def addemoji_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=objectfile.failembed("You can't add an emoji!", "You have to get perms.",
                                                      "Become monkey, become Discord mod."))
            return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num: int, target: typing.Union[discord.Member, discord.User] = None):
        if num > 500 or num < 0:
            return await ctx.send(embed=objectfile.failembed("You can't have above 500 messages cleared.",
                                                             "Or else API will shit itself!", "Sorry."))
        def msgcheck(amsg):
            if target:
                return amsg.author.id == target.id
            return True
        await ctx.channel.purge(limit=num, check=msgcheck)
        embed = objectfile.successembed(f"{ctx.message.author}, I just cleared {num} messages.",
                                        f"See you later, {num} messages.", "Bye.")
        await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=objectfile.failembed("You can't clear!", "You have to get perms.",
                                                      "Become monkey, become Discord mod."))
            return

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        await ctx.send(embed=objectfile.failembed("The owners of this server asked me to leave.",
                                                  "Bye!", "I hope to see you again."))
        await self.bot.get_guild(ctx.message.guild.id).leave()

    @leave.error
    async def leave_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=objectfile.failembed("You can't kick the bot from this server!",
                                                      "You have to get perms.", "Become monkey, "
                                                      "become Discord mod."))
            return


def setup(bot):
    bot.add_cog(Moderation(bot))
