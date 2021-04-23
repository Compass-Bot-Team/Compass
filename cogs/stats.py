# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import gspread
import datetime
import operator
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from utils import embeds, useful_functions, checks
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
servers = useful_functions.servers
validate = useful_functions.validate
credentials = ServiceAccountCredentials.from_json_keyfile_name("antostats.json", scope)
gclient = gspread.authorize(credentials)
spreadsheet = gclient.open("AntoStats")
sheet = spreadsheet.get_worksheet(0)


class Stats(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def monthcount(self, ctx, arg):
        arg = f"1/{arg}"
        messages = {'bot': 0, 'webhook': 0, 'human': 0}
        people = {}
        s_time = time.time()
        m = await ctx.send('Processing messages from a lot of people...')
        p_time = validate(arg)
        a_time = p_time + relativedelta(months=+1)
        print(p_time, a_time)
        n = datetime.datetime.utcnow()
        if p_time.timestamp() > n.timestamp():
            return await ctx.send('That\'s in the future though...')
        async with ctx.channel.typing():
            for c_count, i in enumerate(ctx.guild.text_channels):
                if c_count % 2 == 0:
                    await m.edit(content=f'Processing messages from a lot of people...\n'
                                         f'Scanned {c_count} channel(s) out of {len(ctx.guild.text_channels)}\n'
                                         f'{messages["bot"] + messages["human"] + messages["webhook"]} messages '
                                         f'scanned so far')
                    async for thing in i.history(limit=None, after=p_time):
                        if thing.webhook_id is not None:
                            messages['webhook'] += 1
                        elif thing.author.bot:
                            messages['bot'] += 1
                        elif thing.created_at == a_time.date():
                            break
                        else:
                            messages['human'] += 1
                            try:
                                people[thing.author] += 1
                            except Exception:
                                people[thing.author] = 1
        sorted_people = sorted(people.items(), key=operator.itemgetter(1), reverse=True)
        most_message = [i for i in sorted_people][0]
        await m.edit(content="Calculating stuff.")
        leaderboards = ''
        for count, (user, message) in enumerate(sorted_people):
            if count < 20:
                leaderboards += f"#{count + 1}: {user} ({message} messages)\n"
        await m.delete()
        dur = round(time.time() - s_time)
        await ctx.send(
            f"__**Messages during {p_time.strftime('%m/%d')}**__\n"
            f'Processed {messages["bot"] + messages["human"] + messages["webhook"]} '
            f'messages in {len(ctx.guild.text_channels)} channels from {len(people)} users '
            f'in {dur} seconds ({round(dur / 60, 3)} mins), '
            f'of which {messages["human"]} of them are humans, {messages["webhook"]} of them are webhooks and '
            f'{messages["bot"]} of them are bots. \n'
            f'The human who sent the most messages is {most_message[0]}. They sent {most_message[1]} messages\n'
            f'**__Leaderboard__**\n'
            f'{leaderboards}')

    @commands.cooldown(1, 1, commands.BucketType.guild)
    @checks.not_in_tbk()
    @commands.command()
    async def messagecount(self, ctx, in_time=None):
        messages = {'bot': 0, 'webhook': 0, 'human': 0}
        people = {}
        if in_time is None:
            in_time = datetime.datetime.utcnow().strftime('%d/%m/%Y')
        m = await ctx.send('Processing messages from a lot of people...')
        p_time = validate(in_time)
        n = datetime.datetime.utcnow()
        if p_time.timestamp() > n.timestamp():
            return await ctx.send('That\'s in the future though...')
        async with ctx.channel.typing():
            for c_count, i in enumerate(ctx.guild.text_channels):
                if c_count % 8 == 0:
                    await m.edit(content=f'Processing messages from a lot of people...\n'
                                         f'Scanned {c_count} channel(s) out of {len(ctx.guild.text_channels)}\n'
                                         f'{messages["bot"] + messages["human"] + messages["webhook"]} messages '
                                         f'scanned so far')
                async for thing in i.history(limit=None, after=p_time):
                    if thing.webhook_id is not None and thing.created_at.date() == p_time.date():
                        messages['webhook'] += 1
                    elif thing.author.bot and thing.created_at.date() == p_time.date():
                        messages['bot'] += 1
                    elif thing.created_at.date() == p_time.date():
                        messages['human'] += 1
                        # print(f'message from {thing.author} channel {thing.channel} '
                        #       f'[{messages}/?] at {str(thing.created_at)}')
                        try:
                            people[thing.author] += 1
                        except Exception:
                            people[thing.author] = 1
                    else:
                        break
        sorted_people = sorted(people.items(), key=operator.itemgetter(1), reverse=True)
        await m.edit(content='Calculating stuff.')
        leaderboards = ''
        for count, (user, message) in enumerate(sorted_people):
            if count < 20:
                leaderboards += f"#{count + 1}: {user} ({message} messages)\n"
        await m.delete()
        embed = embeds.embedleader(f"Messages during {p_time.strftime('%Y/%m/%d')}"
                                   f"\nIn {ctx.guild}", ctx.guild.icon_url,
                                   messages["bot"], messages["webhook"], messages["human"],
                                   messages["bot"] + messages["human"] + messages["webhook"])
        if leaderboards == '' or leaderboards is None:
            embed.add_field(name="Leaderboards", value="Nobody sent anything!", inline=False)
            ogmessage = await ctx.send(embed=embed)
        else:
            embed.add_field(name="Leaderboards", value=leaderboards, inline=False)
            ogmessage = await ctx.send(embed=embed)
        d0 = p_time.date()
        d1 = date(2020, 1, 1)
        delta = d1 - d0
        num = delta.days - 2 * delta.days + 2
        if ctx.guild.id in servers:
            sheet.update_cell(int(servers.get(ctx.guild.id)), int(num), str(messages["human"]))
            embed.add_field(name="Your data has been inserted in the sheet.",
                            value="Check it out [**right here!**](http://bit.ly/AntoStatsRaw)", inline=False)
            await ogmessage.edit(embed=embed)
        else:
            embed3 = embeds.twoembed("Sadly, your server is not on our list.",
                                      "If you want us to keep track of your message counts (and other benefits), [**apply here.**](https://bit.ly/AntoStatsForm)")
            await ctx.send(embed=embed3)

    @checks.is_volunteer()
    @commands.command()
    async def allcount(self, ctx, in_time=None):
        pings = []
        if in_time is None:
            in_time = datetime.datetime.utcnow().strftime('%d/%m/%Y')
        p_time = validate(in_time)
        n = datetime.datetime.utcnow()
        if p_time.timestamp() > n.timestamp():
            return await ctx.send('That\'s in the future though...')
        else:
            async with ctx.channel.typing():
                human_messages = 0
                server_left = 0
                m = await ctx.send('Scanning every AntoStats server...')
                for guild in self.bot.guilds:
                    if guild.id in servers:
                        if len(pings) == 0:
                            await m.edit(
                                content=f'''Scanning every AntoStats server...\nI'm scanning {guild.name} at the moment.\nAlso, there's been {human_messages:,} human messages scanned.''')
                        else:
                            await m.edit(
                                content=f'''Scanning every AntoStats server...\nI'm scanning {guild.name} at the moment, and the average amount of time to scan a server is {round(sum(pings) / len(pings), 2):,}ms.\nAlso, there's been {human_messages:,} human messages scanned.''')
                        start = time.perf_counter()
                        messages = 0
                        for c_count, i in enumerate(guild.text_channels):
                            async for thing in i.history(limit=None, after=p_time):
                                if thing.webhook_id is not None and thing.created_at.date() == p_time.date():
                                    pass
                                elif thing.author.bot and thing.created_at.date() == p_time.date():
                                    pass
                                elif thing.created_at.date() == p_time.date():
                                    messages += 1
                                    human_messages += 1
                        d0 = p_time.date()
                        d1 = date(2020, 1, 1)
                        delta = d1 - d0
                        num = delta.days - 2 * delta.days + 2
                        server_left += 1
                        sheet.update_cell(int(servers.get(guild.id)), int(num), str(messages))
                        end = time.perf_counter()
                        pings.append(round((end - start) * 1000))
                await m.edit(embed=embeds.twoembed(f"All messages on {in_time} scanned.",
                                                   f"Check it out [**right here!**](http://bit.ly/AntoStatsRaw)"))


def setup(bot):
    bot.add_cog(Stats(bot))
