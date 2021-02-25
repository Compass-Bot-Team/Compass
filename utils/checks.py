# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import yaml
import discord
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))


class UserSearcher(commands.Converter):
    def get_member(self, ctx, query=None, glb=False):
        if not query:
            return ctx.author
        ret = None
        if query.startswith("<@"):
            query = query.strip("<@!>")  # mention strip
        if query.isdigit() and len(query) >= 15:
            ret = ctx.guild.get_member(int(query))  # id
        if ret is not None:
            return ret
        if "#" in query:
            ret = discord.utils.find(lambda m: f"{m.name}#{m.discriminator}".lower() == query.lower(),
                                     ctx.guild.members)  # name#discrim
        if ret is not None:
            return ret
        ret = discord.utils.find(lambda m: m.name.lower() == query.lower(), ctx.guild.members)  # name
        if ret is not None:
            return ret
        ret = discord.utils.find(lambda m: m.display_name.lower() == query.lower(), ctx.guild.members)  # nickname
        if ret is not None:
            return ret
        if glb:
            if "#" in query:
                ret = discord.utils.find(lambda m: str(m).lower() == query.lower(), ctx.bot.users)
            else:
                query = query.strip("<@!>")
                if query.isdigit() and len(query) >= 15:
                    ret = ctx.bot.get_user(int(query))
                else:
                    ret = None
            if ret is not None:
                return ret
        return None


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
