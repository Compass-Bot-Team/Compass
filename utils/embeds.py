# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import discord
import datetime


def mainembed(header, title1, text1, timestamp=True):
    embed_var = discord.Embed(colour=0x202225, title=str(header), timestamp=datetime.datetime.utcnow())
    embed_var.add_field(name=str(title1), value=str(text1), inline=True)
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var


def twoembed(title1, text1, timestamp=True):
    embed_var = discord.Embed(colour=0x202225, title=str(title1), description=str(text1))
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var


def imgembed(title, url, url2=None, timestamp=True):
    embed_var = discord.Embed(colour=0x202225, title=str(title), timestamp=datetime.datetime.utcnow())
    if url2 is not None:
        embed_var.url = str(url2)
    embed_var.set_image(url=str(url))
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var


def imgembedforzane(title, url, timestamp=True):
    embed_var = discord.Embed(colour=0x202225, url="https://zaneapi.com/", title=str(title),
                              timestamp=datetime.datetime.utcnow())
    embed_var.set_image(url=url)
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var


def imgembedforsrapi(title, url, timestamp=True):
    embed_var = discord.Embed(colour=0x202225, url="https://some-random-api.ml/", title=str(title),
                              timestamp=datetime.datetime.utcnow())
    embed_var.set_image(url=url)
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var


def failembed(title, text, timestamp=True):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title=str(title),
                              description=str(text), timestamp=datetime.datetime.utcnow())
    if timestamp is True:
        embed_var.timestamp = datetime.datetime.utcnow()
    return embed_var

def embedleader(title, url, botval, webval, memval, totalval):
    embedvar = discord.Embed(title=title, color=0x202225)
    embedvar.set_thumbnail(url=url)
    embedvar.add_field(name="Total Messages", value=str(totalval), inline=False)
    embedvar.add_field(name="Bot Messages", value=str(botval), inline=True)
    embedvar.add_field(name="Webhook Messages", value=str(webval), inline=True)
    embedvar.add_field(name="User Messages", value=str(memval), inline=True)
    embedvar.set_footer(text="Support Server: https://discord.gg/SymdusT")
    return embedvar
