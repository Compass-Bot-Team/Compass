import discord
import async_cleverbot
from utils import embeds, checks
from utils.checks import antolib
from discord.ext import commands

support_server_id = 738530998001860629
log_channel_id = 801972292837703708
support_channel_id = 801974601294020609
chatbot_channel_id = 801971149285883955
checkfail = embeds.failembed("You aren't in AntoLib (or you aren't admin there!)", "Try harder.")


class AntoLib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleverbot = async_cleverbot.Cleverbot(self.bot.config['travitiakey'])

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.guild.id != support_server_id:
            return
        if message.author.bot:
            return
        embed = embeds.twoembed(f"Message deleted in #{message.channel}!", message.content)
        embed.add_field(name="Message Author", value=f"<@!{message.author.id}>", inline=True)
        embed.set_thumbnail(url=f"{message.author.avatar_url}")
        logchannel = self.bot.get_channel(log_channel_id)
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.guild.id != support_server_id:
            return
        if before.author.bot:
            return
        embed = embeds.twoembed(f"Message edited in #{before.channel}!", before.content)
        embed.add_field(name="Message Author", value=f"<@!{before.author.id}>", inline=True)
        embed.set_thumbnail(url=f"{before.author.avatar_url}")
        logchannel = self.bot.get_channel(log_channel_id)
        await logchannel.send(embed=embed)

    @antolib()
    @checks.has_admin()
    @commands.command(help="Verifies an unverified member on the AntoLib discord server.")
    async def verify(self, ctx, *, member: discord.Member):
        logchannel = self.bot.get_channel(log_channel_id)
        verifiedrole = discord.utils.get(member.guild.roles, name="Member")
        unverifiedrole = discord.utils.get(member.guild.roles, name="Unverified")
        if unverifiedrole in member.roles:
            await member.add_roles(verifiedrole)
            await member.remove_roles(unverifiedrole)
            embed = embeds.mainembed("User verified.", f"Verified {member}!", f"Action done by {ctx.message.author}")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            await ctx.send(embed=embed)
            await logchannel.send(embed=embed)
        else:
            await ctx.send(embed=embeds.failembed("This user is already verified.", "Get better verification targets ffs", f"Verified Member: {member}"))


def setup(bot):
    bot.add_cog(AntoLib(bot))
