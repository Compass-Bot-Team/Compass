import discord
from utils import embeds, checks, useful_functions
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.command(help="Mass bans a group of users.", aliases=["groupban", "doubleban", "manyban"])
    async def massban(self, ctx, members: commands.Greedy[checks.ModerationUserSearcher], *,
                      reason: commands.clean_content(escape_markdown=True, fix_channel_mentions=True, use_nicknames=True)):
        async with ctx.channel.typing():
            for member in members:
                await ctx.guild.ban(discord.Object(id=member), reason=reason)
        gist = await useful_functions.gist_maker(self.bot.config["githubkey"], f"A massban has occured in {ctx.guild} with the ID {ctx.guild.id}! {len(members):,}/{len(ctx.guild.members):,} members were banned with reason {reason}", "bans", members)
        embed = embeds.twoembed(f"Banned {len(members)} members.",
                                f"Gist output here: {gist}")
        await ctx.send(embed=embed)

    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.command(help="Bans a user.")
    async def ban(self, ctx, member: checks.UserSearcherNoNames, *,
                  reason: commands.clean_content(escape_markdown=True, fix_channel_mentions=True, use_nicknames=True)):
        member = self.bot.get_member(member)
        embed1 = embeds.twoembed(f"You were banned from {ctx.guild}.",
                                 f"Moderator: {ctx.author} ({ctx.author.id})\n"
                                 f"Reason: {reason}")
        embed1.set_thumbnail(url=str(ctx.guild.icon_url))
        await member.send(embed=embed1)
        await ctx.guild.ban(member, reason=reason)
        embed2 = embeds.twoembed(f"{member} ({member.id}) was banned.",
                                 f"Moderator: {ctx.author} ({ctx.author.id})\n"
                                 f"Reason: {reason}")
        embed2.set_thumbnail(url=str(member.icon_url))
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Moderation(bot))
