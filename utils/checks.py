import yaml
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))


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
