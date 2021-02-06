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

import asyncio
import objectfile
import random
from discord.ext import commands


def in_tbk():
    def predicate(ctx):
        if ctx.guild.id == 703420768360595456:
            return True
        else:
            return False
    return commands.check(predicate)

class TBK(commands.Cog, name='TBK Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.tbk = bot.get_guild(703420768360595456)

    @in_tbk()
    @commands.command(help="Time before deletion.", aliases=['tbk_deletion_timer'])
    async def tbkdeletiontimer(self, ctx):
        embed1 = objectfile.newfailembed(f"TBK will be deleted in 10.",
                                         "oh shit")
        embed2 = objectfile.newfailembed(f"TBK will be deleted in 5.",
                                         "oh shit")
        embed3 = objectfile.newfailembed(f"TBK is deleted.",
                                         "oh shit")
        message = await ctx.send(embed=embed1)
        async with ctx.channel.typing():
            await asyncio.sleep(5)
            await message.edit(embed=embed2)
            await asyncio.sleep(5)
            await message.edit(embed=embed3)

    @in_tbk()
    @commands.command(help="List of 10 actives on TBK.", aliases=['tbk_retards'])
    async def tbkretards(self, ctx):
        list_of_retards = []
        tbk = self.bot.get_guild(703420768360595456)
        for degen in tbk.members:
            if tbk.get_role(742633787900559441) and tbk.get_role(705295405256015913) in degen.roles:
                list_of_retards.append(f"<@{str(degen.id)}>")
        list_2 = []
        number = 10
        for _ in range(number):
            retard = random.choice(list_of_retards)
            if retard in list_2:
                return
            else:
                list_2.append(retard)
                number -= 1
        await ctx.send(embed=objectfile.twoembed("TBK's most retarded users!",
                                                 str(list_2).replace("'", "").replace("[", "").replace("]", "")))


def setup(bot):
    bot.add_cog(TBK(bot))