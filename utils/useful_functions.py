# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import aiohttp
import datetime
import operator
import asyncio
import pytz
from discord.ext import commands

logger = logging.getLogger(__name__)

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy", "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia", "wisconsin", "wyoming"]

compasses = ["http://3.bp.blogspot.com/_o3i_gldCzcQ/S_jDEt2qEeI/AAAAAAAAAXI/63fENdJMsGA/s1600/old+compass.jpg",
             "http://cliparts.co/cliparts/8iG/Enn/8iGEnnXrT.jpg",
             "https://i.ytimg.com/vi/wjL_gIRW7TU/maxresdefault.jpg",
             "https://s-media-cache-ak0.pinimg.com/736x/f2/f9/61/f2f961c5fe2bc7c217dd27f5b6e4888d.jpg"]

servers = {
    691668090617987103: 2,
    646424595439550494: 8,
    280051435867996160: 9,
    497514956661587968: 11,
    440500637453647872: 12,
    526308732896935946: 15,
    504557697685782538: 16,
    703420768360595456: 22,
    709199261958668299: 24,
    589563656224899131: 25,
    710192274377801769: 28,
    722263109611421726: 29,
    722609216187138061: 30,
    723808678981140571: 31,
    695450494201495552: 32,
    409654413184073748: 33,
    715547760404856952: 34,
    617669539231956994: 35,
    506036828088827914: 36,
    688026930913738807: 37,
    490851241912565770: 38,
    663079032656494623: 39,
    589274124308840471: 40,
    381522394222690306: 41,
    722061977622675475: 42,
    616743046565855232: 43,
    339948052590624779: 44,
    749573506773286923: 46,
    767658717042180106: 47,
    574647618257420302: 48,
    712797807492202496: 49,
    690112152526389252: 50,
    756708216771051643: 51,
    618426945356431383: 52,
    738530998001860629: 53,
    708999114817536000: 54,
    527645292238209034: 55,
    376407945459662859: 56,
    736359802908836010: 57,
    701454323745292369: 58,
    804473952427835453: 59,
    803105769238167582: 60,
    814229954535489647: 61,
    769762755179446332: 62
}

def validate(date_text):
    try:
        nicething = datetime.datetime.strptime(date_text, "%d/%m/%Y")
        return nicething
    except ValueError:
        print(ValueError)
        return None


async def format_commit(commit):
    # stolen from r.danny
    short, _, _ = commit.message.partition('\n')
    short_sha2 = commit.hex[0:6]
    commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
    commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)
    offset = commit_time.astimezone(pytz.utc).replace(tzinfo=None)
    return f'[`{short_sha2}`](https://github.com/Compass-Bot-Team/Compass/{commit.hex}) {short} at {offset.strftime("%Y-%m-%d %H:%M:%S")}'


async def wait_until(bot):
    while True:
        if bot.not_allocated is False:
            await asyncio.sleep(0.1)
        else:
            return


async def ship(number):
    if number > -1:
        desc = "Heartbroken."
    if number > 25:
        desc = "You will be friendzoned."
    if number > 45:
        desc = "Maybe??"
    if number > 60:
        desc = "Go for it."
    if number > 70:
        desc = "Wow you have a real chance!"
    if number > 80:
        desc = "Make out NOW"
    if number > 90:
        desc = "Monkey sex"
    if number > 95:
        desc = "And that's how I met your mother!"
    return desc


async def users(bot):
    if len(bot.command_users) != 0:
        user_leaderboards_raw = f''
        people = sorted(bot.command_users.items(), key=operator.itemgetter(1), reverse=True)
        for count, (user, commands) in enumerate(people):
            if count < 3:
                user_leaderboards_raw += f'#{count + 1} <@{user}> with {commands} commands used\n'
        return user_leaderboards_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3', '\U0001f949')
    else:
        return None


async def guilds(bot):
    if len(bot.command_guilds) != 0:
        guild_leaderboards_raw = f''
        _servers = sorted(bot.command_guilds.items(), key=operator.itemgetter(1), reverse=True)
        for count, (guild, commands) in enumerate(_servers):
            if count < 3:
                guild_leaderboards_raw += f'#{count + 1} {guild} with {commands} commands used\n'
        return guild_leaderboards_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3', '\U0001f949')
    else:
        return None


async def noliferusers(bot):
    if len(bot.message_senders) != 0:
        no_lifers = sorted(bot.message_senders.items(), key=operator.itemgetter(1), reverse=True)
        no_lifers_raw = f''
        for count, (user, messages) in enumerate(no_lifers):
            if count < 3:
                no_lifers_raw += f'#{count + 1} <@{user}> with {messages} messages sent\n'
        return no_lifers_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3', '\U0001f949')
    else:
        return None


async def noliferguilds(bot):
    if len(bot.guild_senders) != 0:
        guild_leaderboards_raw = f''
        _servers = sorted(bot.guild_senders.items(), key=operator.itemgetter(1), reverse=True)
        for count, (guild, messages) in enumerate(_servers):
            if count < 3:
                guild_leaderboards_raw += f'#{count + 1} {guild} with {messages} messages sent\n'
        return guild_leaderboards_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3', '\U0001f949')
    else:
        return None


async def cogs(bot):
    cogs_list = ''
    cog_count = 0
    for cog in bot.cogs:
        if cog_count == 0:
            cogs_list += f"{cog}"
        else:
            cogs_list += f", {cog}"
        cog_count += 1
    return cogs_list


async def gist_maker(token, description, file_name, file_content, file_type="MD"):
    content = file_content
    if file_type == "MD":
        content = str(f"```python\n{file_content}\n```")
    _json_data = {"description": description,
                  "files": {f"{str(file_name)}.{file_type}": {"content": content}},
                  "public": False}
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post("https://api.github.com/gists", json=_json_data) as raw_get:
            _json = await raw_get.json()
    return _json["html_url"]


async def number_poll(message, num=None):
    if num is None:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000037\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000038\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000039\U0000fe0f\U000020e3")
        await message.add_reaction("\U0001f51f")
        return
    if num == 1:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
    if num == 2:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
    if num == 3:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
    if num == 4:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
    if num == 5:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
    if num == 6:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
    if num == 7:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000037\U0000fe0f\U000020e3")
    if num == 8:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000037\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000038\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000039\U0000fe0f\U000020e3")
    if num == 9:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000037\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000038\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000039\U0000fe0f\U000020e3")
    if num == 10:
        await message.add_reaction('\U00000031\U0000fe0f\U000020e3')
        await message.add_reaction('\U00000032\U0000fe0f\U000020e3')
        await message.add_reaction("\U00000033\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000034\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000035\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000036\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000037\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000038\U0000fe0f\U000020e3")
        await message.add_reaction("\U00000039\U0000fe0f\U000020e3")
        await message.add_reaction("\U0001f51f")


async def poll_classic(message):
    await message.add_reaction('\U0001F7E9')
    await message.add_reaction('\U0001F7E8')
    await message.add_reaction('\U0001F7E5')
    await message.add_reaction("\U0001F7EA")
    await message.add_reaction("\u2754")
