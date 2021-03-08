# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math
import traceback
import discord
import asyncio
from discord.ext import commands
from utils import exceptions
from utils.useful_functions import gist_maker
from utils.embeds import failembed


async def error_handle(bot, error, ctx):
    if hasattr(ctx.command, 'on_error'):
        return
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return
    error = getattr(error, 'original', error)
    idc = (commands.CommandNotFound, asyncio.TimeoutError)
    if isinstance(error, idc):
        return
    if isinstance(error, commands.ExtensionNotLoaded):
        return await ctx.send(embed=failembed("Cog not loaded!", error))
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=failembed("Missing required argument!", error))
    if isinstance(error, commands.CheckFailure):
        return await ctx.send(embed=failembed("Missing a check!", error))
    if isinstance(error, commands.NotOwner):
        return await ctx.send(embed=failembed("You aren't the owner!", "Nice try."))
    if isinstance(error, commands.CommandOnCooldown):
        num = math.ceil(error.retry_after)
        total = f"{num:,.2f} seconds ({round((num / 60), 2):,.2f} minutes)."
        return await ctx.send(embed=failembed(f"Try again in {total}",
                                              f"Cool down bro!"))
    if isinstance(error, commands.MemberNotFound):
        return await ctx.send(embed=failembed(error, "Try again with someone else!"))
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=failembed("I don't have perms or I was hierarchy'd.", "Give me permissions pwease!"))
    if isinstance(error, exceptions.ImageManipulationError):
        return await ctx.send(embed=failembed("Error in image manipulation!", error))
    bad_arguments = (commands.BadArgument, commands.BadUnionArgument, commands.BadBoolArgument, commands.BadColourArgument, commands.BadInviteArgument)
    if isinstance(error, bad_arguments):
        return await ctx.send(embed=failembed("Bad argument!", error))
    if isinstance(error, commands.TooManyArguments):
        return await ctx.send(embed=failembed("Too many arguments!", error))
    else:
        DTOG = bot.get_user(bot.config["owners"][0])
        traceback_text = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        embed = failembed(f"Unaccounted error!", error)
        embed.add_field(name="Checklist", value="Sent to Owner: <:compass_bot_yes:809974729136930836>")
        await ctx.send(embed=embed)
        try:
            return await DTOG.send(embed=failembed(f"Error in {ctx.command}!",
                                                   f"```python\n{traceback_text}\n```"))
        except discord.errors.HTTPException:
            gist = await gist_maker(bot.config["githubkey"], f"Error in {ctx.command}!", "ERROR", traceback_text)
            return await DTOG.send(embed=failembed(f"Error in {ctx.command}!",
                                                   f"[The text was too long to be posted, so I sent it to "
                                                   f"**gist.github.com** for you.]({gist})"))


class ErrorHandling(commands.Cog, name='Error Handling', description='The error handling cog for Compass.'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_command_error')
    async def error_handling(self, ctx, error):
        await ctx.message.add_reaction("<:compass_bot_no:809974728915419177>")
        return await error_handle(self.bot, error, ctx)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
