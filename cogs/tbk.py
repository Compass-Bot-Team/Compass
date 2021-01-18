import discord
import asyncio
import objectfile
import random
from discord.ext import commands


def in_tbk():
    def predicate(ctx):
        return ctx.guild.id == 703420768360595456
    return commands.check(predicate)

class TBK(commands.Cog, name='TBK Commands'):
    def __init__(self, bot):
        self.bot = bot
        self.tbk = bot.get_guild(703420768360595456)

    async def timer(self, second):
        if second == 0:
            embed = objectfile.newfailembed(f"TBK is deleted.",
                                            "oh shit")
        else:
            embed = objectfile.newfailembed(f"TBK is deleted in {second}.",
                                            "oh shit")
        await asyncio.sleep(1)
        return embed

    @in_tbk()
    @commands.command(aliases=['tbk_deletion_timer'])
    async def tbkdeletiontimer(self, ctx):
        second = 10
        message = await ctx.send(embed=await self.timer(second))
        second -= 1
        for _ in range(10):
            await message.edit(embed=await self.timer(second))
            second -= 1

    @in_tbk()
    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.command(aliases=['tbk_retards'])
    async def tbkretards(self, ctx):
        list_of_retards = []
        tbk = self.bot.get_guild(703420768360595456)
        for degen in tbk.members:
            if tbk.get_role(742633787900559441) and tbk.get_role(705295405256015913) in degen.roles:
                list_of_retards.append(f"<@{str(degen.id)}>")
        list_2 = []
        number = 10
        for _ in range(10):
            retard = random.choice(list_of_retards)
            if retard in list_2:
                return
            else:
                list_2.append(retard)
                number -= 1
        await ctx.send(embed=objectfile.twoembed("the hit list",
                                                 str(list_2).replace("'", "").replace("[", "").replace("]", "")))


def setup(bot):
    bot.add_cog(TBK(bot))