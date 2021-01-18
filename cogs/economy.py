import discord
import random
import asyncio
import objectfile
import json
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_account_data():
        with open("bank.json", "r") as f:
            users = json.load(f)
        return users

    async def open_account(self, user):
        users = self.get_account_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

    @staticmethod
    def get_robbed_user():
        with open("bank.json", "r") as f:
            robbed_user = json.load(f)
        return robbed_user

    @commands.command()
    async def balance(self, ctx):
        await self.open_account(ctx.message.author)
        user = ctx.message.author
        users = self.get_account_data()

        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]

        await ctx.send(embed=objectfile.walletembed(f"{ctx.message.author.name}'s Balance", "Wallet  \U0001f45b",
                                                    f"{wallet}",
                                                    "Bank  \U0001f3e6",
                                                    f"{bank}"))

    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.command()
    async def work(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = self.get_account_data()
        moneygained = random.randint(1, 200)
        users[str(user.id)]["wallet"] += moneygained

        with open("bank.json", "w") as f:
            json.dump(users, f)

        workplaces = ["coded for Compass", 'worked in the Chinese "factories"', "redistributed the wealth"]
        message = random.choice(workplaces)

        await ctx.send(embed=objectfile.workembed(f"You're a hard worker, {ctx.message.author.name}.",
                                                  f"You {message} and gained {moneygained} coins!",
                                                  "GG."))

    @commands.command()
    async def russianroulette(self, ctx):
        agreemessage = await ctx.send(embed=objectfile.twoembed("If you lose the game you will be kicked.",
                                                                "React with \U00002705 if you agree!"))
        await agreemessage.add_reaction('\U00002705')
        await agreemessage.add_reaction('\U0000274c')

        def check(reaction, author):
            return author == ctx.message.author and str(reaction.emoji) in ['\U00002705', '\U0000274c']

        try:
            reac, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed=objectfile.twoembed("Timed out",
                                                     "The Russian Roulette request timed out after inactivity."))
        else:
            if str(reac.emoji) == '\U00002705':
                randomchoice = int((random.randint(0, 100)))
                if randomchoice < 50:
                    loser = ctx.message.author
                    invite = await ctx.message.channel.create_invite(max_age=0, max_uses=0, reason="User lost Russian Roulette.")
                    await ctx.send(embed=objectfile.twoembed("This guy lost.",
                                                             "He is dead!"))
                    await loser.send(embed=objectfile.twoembed("You lost.",
                                                              "You are dead!\n"
                                                              f"Server invite link; {invite}"))
                    await loser.kick()
                if randomchoice > 50:
                    user = ctx.author
                    users = self.get_account_data()
                    moneygained = random.randint(1, 200)
                    users[str(user.id)]["wallet"] += moneygained

                    with open("bank.json", "w") as f:
                        json.dump(users, f)

                    await ctx.send(embed=objectfile.twoembed("You survived.",
                                                             f"As a reward, you gained {moneygained}.\n"
                                                             f"Go again with compass!russianroulette!"))

    @commands.command()
    async def deposit(self, ctx, *, arg):
        user = ctx.author
        users = self.get_account_data()
        if users[str(user.id)]["wallet"] < 0:
            await ctx.send(embed=objectfile.twoembed("You don't have any depositable money!",
                                                     "You're broke or you have it all deposited already."))
        else:
            users[str(user.id)]["bank"] += users[str(user.id)]["wallet"]
            users[str(user.id)]["wallet"] -= users[str(user.id)]["bank"]

            with open("bank.json", "w") as f:
                json.dump(users, f)

            await ctx.send(embed=objectfile.twoembed(f"You've deposited.",
                                                     f"Your moneys are safe."))

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        user = ctx.author
        users = self.get_account_data()
        moneygained = random.randint(1, 500)
        users[str(user.id)]["wallet"] += moneygained

        with open("bank.json", "w") as f:
            json.dump(users, f)

        await ctx.send(embed=objectfile.twoembed("You've gotten your daily reward.",
                                                 f"As a reward, you gained {moneygained}."))

    @commands.cooldown(1, 7200)
    @commands.command()
    async def rob(self, ctx, robbed: discord.User):
        user = ctx.author
        users = self.get_account_data()
        robbed_user = self.get_robbed_user()
        robbed_user_wallet = robbed_user[str(robbed.id)["wallet"]]
        robbedchance = random.randint(1, 100)
        moneygainedorlost = random.randint(1, robbed_user_wallet)
        if robbed_user_wallet < 0:
            await ctx.send(embed=objectfile.twoembed("This user has no money!",
                                                     "They are either broke or have it all stored."))
        else:
            if robbedchance < 50:
                users[str(user.id)]["wallet"] -= moneygainedorlost

                with open("bank.json", "w") as f:
                    json.dump(users, f)

                await ctx.send(embed=objectfile.twoembed("You've fucked up.",
                                                         f"You just lost {moneygainedorlost}."))
            if robbedchance > 50:
                users[str(user.id)]["wallet"] += moneygainedorlost
                robbed_user_wallet -= moneygainedorlost

                with open("bank.json", "w") as f:
                    json.dump(users, f)
                with open("bank.json", "w") as f:
                    json.dump(robbed_user, f)

                await ctx.send(embed=objectfile.twoembed(f"You've robbed {moneygainedorlost}.",
                                                         f"I feel bad for {robbed}."))


def setup(bot):
    bot.add_cog(Economy(bot))
