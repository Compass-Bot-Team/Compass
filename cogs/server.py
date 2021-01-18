import discord
import objectfile
import sr_api
from bot import has_admin
from datetime import datetime
from discord.ext import commands
from discord.utils import get

client = sr_api.Client()
support_server_id = 773318789617811526

def in_compass_server():
    def predicate(ctx):
        return ctx.guild.id == 773318789617811526
    return commands.check(predicate)

class Compass_Server(commands.Cog, name='Compass Server Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logchannel = self.bot.get_channel(777039726506934273)
        if not member.guild.id == support_server_id:
            return
        else:
            entrance = self.bot.get_channel(777278788437278742)
            embed = objectfile.twoembed(f"{member} has joined the server!",
                                        "Give them a warm welcome.")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_footer(text=datetime.now())
            await entrance.send(embed=embed)
            await logchannel.send(embed=embed)
            created_at = member.created_at
            time_now = datetime.now()
            calc = (time_now - created_at)
            if calc.days < 60:
                unverifiedrole = get(member.guild.roles, name="Unverified")
                await member.add_roles(unverifiedrole)
                verification_channel = self.bot.get_channel(784123330281472061)
                embed = objectfile.twoembed("Please answer the questions posted "
                                            "to enter the rest of the server.",
                                            "\n\n1. Where did you find the "
                                            "invite to the server?\n "
                                            "2. Was the Compass Bot "
                                            "in a server of your "
                                            "creation or did you see "
                                            "it in a server?\n "
                                            "3. Did you read the "
                                            "rules (name one, "
                                            "if so)?\n "
                                            "4. When did you join "
                                            "Discord?")
                embed.set_thumbnail(url=f"{member.avatar_url}")
                embed.set_footer(text=datetime.now())
                await verification_channel.send(f"<@{member.id}>", embed=embed)
                embed = objectfile.twoembed(f"{member} was under 60 days of age on Discord.",
                                            "As such, they have been put in the verification system.")
                embed.set_thumbnail(url=f"{member.avatar_url}")
                embed.set_footer(text=datetime.now())
                await logchannel.send(embed=embed)
            if calc.days > 60:
                verifiedrole = get(member.guild.roles, name="Member")
                await member.add_roles(verifiedrole)
                embed = objectfile.twoembed(f"{member} was over 60 days of age on Discord.",
                                            "As such, they have been automatically verified.")
                embed.set_thumbnail(url=f"{member.avatar_url}")
                embed.set_footer(text=datetime.now())
                await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        logchannel = self.bot.get_channel(777039726506934273)
        if not member.guild.id == support_server_id:
            return
        else:
            entrance = self.bot.get_channel(777278788437278742)
            embed = objectfile.twoembed(f"{member} has left the server.",
                                        "Cya later.")
            embed.set_footer(text=datetime.now())
            embed.set_thumbnail(url=f"{member.avatar_url}")
            await entrance.send(embed=embed)
            await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.guild.id != support_server_id:
            return
        if message.author.bot:
            return
        if message.channel.id == 783704808225505281:
            chatbot = await client.chatbot(str(message.content))
            channel = self.bot.get_channel(783704808225505281)
            embed = objectfile.twoembed(f"{chatbot}", f"Processed: {str(message.content)}")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.guild.id != support_server_id:
            return
        if message.author.bot:
            return
        embed = discord.Embed(title=f"Message deleted in #{message.channel}!",
                              description=f"Message from <@!{message.author.id}>",
                              color=discord.Color.from_rgb(122, 141, 207))
        embed.add_field(name="Message", value=message.content)
        embed.set_footer(text=f"{message.created_at}")
        embed.set_thumbnail(url=f"{message.author.avatar_url}")
        logchannel = self.bot.get_channel(777039726506934273)
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        author = before.author
        if not before.guild or before.guild.id != support_server_id:
            return
        if before.author.bot:
            return
        embed = discord.Embed(title=f"Message edited in #{before.channel}!",
                              description=f"Message from <@!{before.author.id}>",
                              color=discord.Color.from_rgb(122, 141, 207))
        embed.add_field(name="Message Before", value=f"{before.content}", inline=True)
        embed.add_field(name="Message After", value=f"{after.content}", inline=True)
        embed.set_footer(text=f"{datetime.now()}")
        embed.set_thumbnail(url=f"{author.avatar_url}")
        logchannel = self.bot.get_channel(777039726506934273)
        await logchannel.send(embed=embed)

    @in_compass_server()
    @has_admin()
    @commands.command()
    async def verify(self, ctx, member: discord.Member):
        logchannel = self.bot.get_channel(777039726506934273)
        verifiedrole = get(member.guild.roles, name="Member")
        unverifiedrole = get(member.guild.roles, name="Unverified")
        if unverifiedrole in member.roles:
            await member.add_roles(verifiedrole)
            await member.remove_roles(unverifiedrole)
            embed = objectfile.successembed("User verified.",
                                            f"Verified {member}!",
                                            f"Action done by {ctx.message.author}")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            await ctx.send(embed=embed)
            await logchannel.send(embed=embed)
        else:
            await ctx.send(embed=objectfile.failembed("This user is already verified.",
                                                      "Get better verification targets ffs",
                                                      f"Verified Member: {member}"))

    @in_compass_server()
    @has_admin()
    @commands.command(hidden=True)
    async def rules(self, ctx):
        embed = discord.Embed(colour=discord.Color.from_rgb(122, 141, 207), title="The Rules")
        embed.add_field(name="Rule 1 - Common Sense",
                        value="Use common sense on the server. This should make sense but just don't act dumb.",
                        inline=False)
        embed.add_field(name="Rule 2 - Follow the ToS",
                        value="Don't raid the server or post NSFW, and especially don't be underage.", inline=False)
        embed.add_field(name="Rule 3 - Use the right channels",
                            value="Use the right channels, don't post bug reports in general chat.", inline=False)
        embed.add_field(name="Rule 4 - No harassment",
                        value="This should come with Rule 1 and 2, but don't harass anyone.", inline=False)
        embed.add_field(name="Rule 5 - Hard R is Banned", value="Don't post the Hard R.", inline=False)
        await ctx.send(embed=embed)

        # About the Server
        embed2 = discord.Embed(colour=discord.Color.from_rgb(122, 141, 207), title="About the Server")
        embed2.add_field(name="Server Information",
                         value="The Compass server is the official server for the Compass bot and its projects.",
                         inline=False)
        embed2.add_field(name="About the Compass Team",
                             value="Compass is a team of Python, HTML, and CSS developers that "
                               "specialize mostly in creating Discord bots.",
                         inline=True)
        embed2.add_field(name="About the Compass Bot",
                         value="The Compass Bot is an all-in-one bot coded in the discord.py library.\n"
                               "Website: https://compasswebsite.dev\n"
                               "Invite: Just [click here!](https://discord.com/oauth2/authorize?client_id"
                               "=769308147662979122&permissions=2147352567&scope=bot)\n"
                               "Documentation: Just [click here!](https://github.com/Compass-Bot-Team/"
                               "Compass-Documentation/blob/main/README.md)")
        await ctx.send(embed=embed2)
        # Self roles
        embed3 = discord.Embed(colour=discord.Color.from_rgb(122, 141, 207), title="Bot Update Ping",
                               description="React with \U0001f3d3 for the <@&784975287392665611>")
        selfrolemessage = await ctx.send(embed=embed3)
        await selfrolemessage.add_reaction('\U0001f3d3')


def setup(bot):
    bot.add_cog(Compass_Server(bot))
