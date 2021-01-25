import aiosqlite
import asyncio
import objectfile
from bot import has_admin
from discord.ext import commands

class Aiosqlite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        try:
            async with aiosqlite.connect('databases/compassdb.db') as db:
                async with db.execute("SELECT * FROM Memes ORDER BY RANDOM() LIMIT 1;") as cursor:
                    get_info = await cursor.fetchone()
                    author = get_info[1]
                    linkcalc = str(get_info[0]).replace("('", "").replace(")", "").replace("%27,", "").replace("',", "")
                    await ctx.send(f"Your meme!\nSubmitted by {author}\n\n{linkcalc}")
        except aiosqlite.Error:
            async with aiosqlite.connect('databases/compassdb.db') as db:
                await db.execute('''CREATE TABLE Memes (link, author)''')
                await db.commit()
            await ctx.send("No memes in the table, try again later.")

    @has_admin()
    @commands.command()
    async def addmeme(self, ctx, *, link:str):
        try:
            async with aiosqlite.connect('databases/compassdb.db') as db:
                await db.execute(f"""INSERT INTO Memes VALUES ("{link}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")
        except aiosqlite.Error:
            async with aiosqlite.connect('databases/compassdb.db') as db:
                await db.execute('''CREATE TABLE Memes (link, author)''')
                await asyncio.sleep(0.1)
                await db.execute(f"""INSERT INTO Memes VALUES ("{link}", "{ctx.author.name}#{ctx.author.discriminator}");""")
                await db.commit()
                await ctx.send(f"Success!")

def setup(bot):
    bot.add_cog(Aiosqlite(bot))