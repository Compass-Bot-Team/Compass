# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import yaml
import discord
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))


class UserSearcher(commands.Converter):
    async def convert(self, ctx, argument):
        if ctx.guild is None:
            raise commands.BadArgument("This command does not work in DMs!")
        glb = True
        ret = None
        if argument.startswith("<@"):
            argument = argument.strip("<@!>")  # mention strip
        if argument.isdigit() and len(argument) >= 15:
            ret = ctx.guild.get_member(int(argument))  # id
        if ret is not None:
            return ret
        elif "#" in argument:
            ret = discord.utils.find(lambda m: f"{m.name}#{m.discriminator}".lower() == argument.lower(),
                                     ctx.guild.members)  # name#discrim
        if ret is not None:
            return ret
        else:
            ret = discord.utils.find(lambda m: m.name.lower() == argument.lower(), ctx.guild.members)  # name
        if ret is not None:
            return ret
        else:
            ret = discord.utils.find(lambda m: m.display_name.lower() == argument.lower(),
                                     ctx.guild.members)  # nickname
        if ret is not None:
            return ret
        if glb:
            if "#" in argument:
                ret = discord.utils.find(lambda m: str(m).lower() == argument.lower(), ctx.bot.users)
            if ret is not None:
                return ret
            else:
                argument = argument.strip("<@!>")
                if argument.isdigit() and len(argument) >= 15:
                    ret = ctx.bot.get_user(int(argument))
                else:
                    ret = None
            if ret is not None:
                return ret
        raise commands.MemberNotFound(argument)


class ModerationUserSearcher(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.startswith("<@"):
            argument = argument.strip("<@!>")
        try:
            arg = int(argument)
        except ValueError:
            raise commands.MemberNotFound(argument)
        else:
            return arg


class UserSearcherNoNames(commands.Converter):
    async def convert(self, ctx, argument):
        if ctx.guild is None:
            raise commands.BadArgument("This command does not work in DMs!")
        ret = None
        if argument.startswith("<@"):
            argument = argument.strip("<@!>")  # mention strip
        if argument.isdigit() and len(argument) >= 15:
            ret = ctx.guild.get_member(int(argument))  # id
        else:
            ret = None
        if ret is not None:
            if ret is not ctx.author:
                return ret
            else:
                raise commands.BadArgument("You can't do mod actions against yourself!")
        raise commands.MemberNotFound(argument)


class UserOrGuild(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            argument = int(argument)
        except ValueError:
            raise commands.BadArgument(f"{argument} is not a valid integer!")
        else:
            bot = ctx.bot
            try:
                user = bot.get_user(argument)
            except Exception:
                try:
                    guild = bot.get_guild(argument)
                except Exception:
                    raise commands.BadArgument(f"No matching user or guild with ID {int(argument)}!")
                else:
                    return ["guild", guild]
            else:
                return ["user", user]


def antolib():
    def predicate(ctx):
        return ctx.guild.id == 738530998001860629

    return commands.check(predicate)


def has_admin():
    def predicate(ctx):
        bot = ctx.bot
        guild = bot.get_guild(738530998001860629)
        role = guild.get_role(793211817174237215)
        list_of_ids = []
        for member in role.members:
            list_of_ids.append(member.id)
        if ctx.author.id in list_of_ids or ctx.author.id in config["owners"]:
            return True
        else:
            return False

    return commands.check(predicate)


def meme_quote_perms():
    def predicate(ctx):
        bot = ctx.bot
        guild = bot.get_guild(738530998001860629)
        role = guild.get_role(793211817174237215)
        list_of_ids = []
        for member in role.members:
            list_of_ids.append(member.id)
        if ctx.author.id in list_of_ids or ctx.author.id in config["owners"] or ctx.author.id in config["whitelisted"]:
            return True
        else:
            return False
    return commands.check(predicate)


def globus_admin():
    def predicate(ctx):
        bot = ctx.bot
        guild = bot.get_guild(784126280089337887)
        role = guild.get_role(784127369492299788)
        if ctx.author.id in [member.id for member in role]:
            return True
        else:
            return False
    return commands.check(predicate)
