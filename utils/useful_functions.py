# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import aiohttp
import datetime
import operator
import asyncio
import pytz
import json
import os

directory = os.getcwd()
logger = logging.getLogger(__name__)

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
          "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
          "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "Alabama", "Alaska",
          "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Hawaii", "Idaho",
          "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
          "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
          "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
          "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "al", "ak", "az", "ar", "ca", "co", "ct",
          "dc", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms",
          "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn",
          "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy", "alabama", "alaska", "arizona", "arkansas", "california",
          "colorado", "connecticut", "delaware", "florida", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas",
          "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
          "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york",
          "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island",
          "south carolina", "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington",
          "west virginia", "wisconsin", "wyoming"]

compasses = ["http://3.bp.blogspot.com/_o3i_gldCzcQ/S_jDEt2qEeI/AAAAAAAAAXI/63fENdJMsGA/s1600/old+compass.jpg",
             "http://cliparts.co/cliparts/8iG/Enn/8iGEnnXrT.jpg",
             "https://i.ytimg.com/vi/wjL_gIRW7TU/maxresdefault.jpg",
             "https://s-media-cache-ak0.pinimg.com/736x/f2/f9/61/f2f961c5fe2bc7c217dd27f5b6e4888d.jpg"]

states = [{"name": "Alabama", "status": "Republican", "electors": 9, "location": (650, 398)},
          {"name": "Alaska", "status": "Republican", "electors": 3, "location": (92, 510)},
                   {"name": "Arizona", "status": "Swing", "electors": 11, "location": (201, 367)},
                   {"name": "Arkansas", "status": "Republican", "electors": 6, "location": (559, 357)},
                   {"name": "California", "status": "Democratic", "electors": 54, "location": (85, 322)},
                   {"name": "Colorado", "status": "Swing", "electors": 10, "location": (275, 256)},
                   {"name": "Connecticut", "status": "Democratic", "electors": 7, "location": (852, 173)},
                   {"name": "Delaware", "status": "Democratic", "electors": 3, "location": (828, 250)},
                   {"name": "Florida", "status": "Swing", "electors": 30, "location": (752, 467)},
                   {"name": "Georgia", "status": "Swing", "electors": 16, "location": (710, 393)},
                   {"name": "Hawaii", "status": "Democratic", "electors": 4, "location": (331, 558)},
                   {"name": "Idaho", "status": "Republican", "electors": 4, "location": (175, 121)},
                   {"name": "Illinois", "status": "Democratic", "electors": 20, "location": (600, 258)},
                   {"name": "Indiana", "status": "Republican", "electors": 11, "location": (651, 234)},
                   {"name": "Iowa", "status": "Swing", "electors": 6, "location": (538, 219)},
                   {"name": "Kansas", "status": "Republican", "electors": 6, "location": (465, 315)},
                   {"name": "Kentucky", "status": "Republican", "electors": 8, "location": (660, 310)},
                   {"name": "Louisiana", "status": "Republican", "electors": 8, "location": (539, 439)},
                   {"name": "Maine-At-Large", "status": "Democratic", "electors": 2, "location": (887, 82)},
                   {"name": "Maine-District 1", "status": "Democratic", "electors": 1, "location": (892, 113)},
                   {"name": "Maine-District 2", "status": "Swing", "electors": 1, "location": (887, 58)},
                   {"name": "Maryland", "status": "Democratic", "electors": 10, "location": (822, 257)},
                   {"name": "Massachusetts", "status": "Democratic", "electors": 11, "location": (856, 157)},
                   {"name": "Michigan", "status": "Swing", "electors": 15, "location": (673, 199)},
                   {"name": "Minnesota", "status": "Swing", "electors": 10, "location": (495, 139)},
                   {"name": "Mississippi", "status": "Republican", "electors": 6, "location": (603, 416)},
                   {"name": "Missouri", "status": "Republican", "electors": 10, "location": (533, 295)},
                   {"name": "Montana", "status": "Republican", "electors": 4, "location": (277, 78)},
                   {"name": "Nebraska-At-Large", "status": "Republican", "electors": 2, "location": (414, 224)},
                   {"name": "Nebraska-District 1", "status": "Republican", "electors": 1, "location": (462, 224)},
                   {"name": "Nebraska-District 2", "status": "Swing", "electors": 1, "location": (476, 230)},
                   {"name": "Nebraska-District 3", "status": "Republican", "electors": 1, "location": (442, 200)},
                   {"name": "Nevada", "status": "Swing", "electors": 6, "location": (141, 213)},
                   {"name": "New Hampshire", "status": "Swing", "electors": 4, "location": (864, 136)},
                   {"name": "New Jersey", "status": "Democratic", "electors": 14, "location": (833, 226)},
                   {"name": "New Mexico", "status": "Swing", "electors": 5, "location": (287, 397)},
                   {"name": "New York", "status": "Democratic", "electors": 29, "location": (805, 138)},
                   {"name": "North Carolina", "status": "Swing", "electors": 16, "location": (778, 329)},
                   {"name": "North Dakota", "status": "Republican", "electors": 3, "location": (398, 107)},
                   {"name": "Ohio", "status": "Swing", "electors": 17, "location": (684, 234)},
                   {"name": "Oklahoma", "status": "Republican", "electors": 7, "location": (446, 375)},
                   {"name": "Oregon", "status": "Democratic", "electors": 8, "location": (107, 114)},
                   {"name": "Pennsylvania", "status": "Swing", "electors": 19, "location": (765, 205)},
                   {"name": "Rhode Island", "status": "Democratic", "electors": 4, "location": (877, 172)},
                   {"name": "South Carolina", "status": "Republican", "electors": 9, "location": (767, 377)},
                   {"name": "South Dakota", "status": "Republican", "electors": 3, "location": (436, 152)},
                   {"name": "Tennessee", "status": "Republican", "electors": 11, "location": (627, 347)},
                   {"name": "Texas", "status": "Swing", "electors": 40, "location": (474, 474)},
                   {"name": "Utah", "status": "Republican", "electors": 6, "location": (237, 237)},
                   {"name": "Vermont", "status": "Democratic", "electors": 3, "location": (844, 116)},
                   {"name": "Virginia", "status": "Swing", "electors": 13, "location": (802, 283)},
                   {"name": "Washington", "status": "Democratic", "electors": 12, "location": (125, 56)},
                   {"name": "Washington D.C.", "status": "Democratic", "electors": 3, "location": (803, 248)},
                   {"name": "West Virginia", "status": "Republican", "electors": 5, "location": (784, 245)},
                   {"name": "Wisconsin", "status": "Swing", "electors": 10, "location": (577, 169)},
                   {"name": "Wyoming", "status": "Republican", "electors": 3, "location": (266, 166)}]
biden_states = ["California", "Oregon", "Washington", "Arizona", "New Mexico", "California", "Minnesota",
                "Wisconsin", "Illinois", "Michigan", "Georgia", "Pennsylvania", "Virginia", "Maryland",
                "Washington D.C.", "Delaware", "New Jersey", "New York", "Connecticut", "Rhode Island",
                "Massachusetts", "New Hampshire", "Vermont", "Maine-At-Large", "Hawaii", "Nevada", "Maine-District 1",
                "Nebraska-District 2", "Colorado"]


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
        return guild_leaderboards_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3',
                                                                                                      '\U0001f949')
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
        return guild_leaderboards_raw.replace('#1', '\U0001f947').replace('#2', '\U0001f948').replace('#3',
                                                                                                      '\U0001f949')
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


async def loc_finder():
    proc = await asyncio.create_subprocess_shell(f"cloc --json {directory}",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stdout:
        results = f'{stdout.decode()}'
    elif stderr:
        results = f'{stderr.decode()}'
    json_cloc = json.loads(str(results))
    return json_cloc["header"]["n_lines"]
