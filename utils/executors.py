# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import wikipedia
import gtts
import random
import utils.embeds as embeds
from utils.useful_functions import states, biden_states
from PIL import Image, ImageDraw


def tts(text):
    _bytes = io.BytesIO()
    speech = gtts.gTTS(text)
    speech.write_to_fp(_bytes)
    _bytes.seek(0)
    return _bytes


def wikipedia_exec(page: str):
    page = page.replace("joe biden n", "joe biden")
    wikipedia.set_lang("en")
    result = wikipedia.search(f"{page}")
    return [result.url, result.title, wikipedia.summary(f"{page}", sentences=2)]


def electiongenerator(mode):
    democratic_nebraska_districts = 0
    republican_nebraska_districts = 0
    democratic_electors = 0
    republican_electors = 0
    republican_states = []
    democrat_states = []
    democratic_electors_2020 = 306
    republican_electors_2020 = 232
    landslide_victor = random.randint(1, 2)
    map = Image.open("Map.png").convert('RGB')
    democrat_color = (16, 48, 114)
    democrat_flip_color = (37, 93, 130)
    republican_color = (132, 17, 20)
    republican_flip_color = (191, 29, 41)
    if mode == "Normal":
        unrealistic = False
        landslide = False
    if mode == "Unrealistic":
        unrealistic = True
        landslide = False
    if mode == "Landslide":
        unrealistic = False
        landslide = True
    for state in states:
        name = state["name"]
        if name != "Nebraska-At-Large" or "Maine-At-Large":
            status = state["status"]
            if landslide is True:
                if landslide_victor == 1:
                    if status == "Swing":
                        status = "Republican"
                    elif status == "Democratic":
                        status = "Swing"
                elif landslide_victor == 2:
                    if status == "Swing":
                        status = "Democratic"
                    elif status == "Republican":
                        status = "Swing"
            elif unrealistic is True:
                unrealistic_victor = random.randint(1, 2)
                if unrealistic_victor == 1:
                    if status == "Swing":
                        status = "Republican"
                    elif status == "Democratic":
                        status = "Swing"
                elif unrealistic_victor == 2:
                    if status == "Swing":
                        status = "Democratic"
                    elif status == "Republican":
                        status = "Swing"
            if status == "Swing":
                coin_toss = random.randint(1, 2)
                if coin_toss == 1:
                    if name.startswith("Nebraska-District "):
                        republican_nebraska_districts += 1
                    republican_states.append(name)
                elif coin_toss == 2:
                    if name.startswith("Nebraska-District "):
                        democratic_nebraska_districts += 1
                    democrat_states.append(name)
            elif status == "Republican":
                republican_states.append(name)
            elif status == "Democratic":
                democrat_states.append(name)
        state["color"] = (republican_color if state["name"] in republican_states else democrat_color)
    for state in states:
        ImageDraw.floodfill(map, xy=state["location"],
                            value=state["color"])
        if name == "Nebraska-At-Large":
            if republican_nebraska_districts > democratic_nebraska_districts:
                democrat_states.remove("Nebraska-At-Large")
                republican_states.append("Nebraska-At-Large")
        if name == "Maine-At-Large":
            if "Maine-District 1" or "**Maine-District 1**" in republican_states and "Maine-At-Large" not in republican_states:
                democrat_states.remove("Maine-At-Large")
                republican_states.append("Maine-At-Large")
                republican_electors += 2
            elif "Maine-District 1" and "**Maine-District 1**" not in republican_states and "Maine-At-Large" in republican_states:
                democrat_states.remove("Maine-At-Large")
                republican_states.append("Maine-At-Large")
        if state["name"] in democrat_states:
            democratic_electors += state["electors"]
            if state["name"] not in biden_states:
                democrat_states.remove(state["name"])
                democrat_states.append("**"+state["name"]+"**")
                ImageDraw.floodfill(map, xy=state["location"],
                                    value=democrat_flip_color)
            else:
                ImageDraw.floodfill(map, xy=state["location"],
                                    value=state["color"])
        elif state["name"] in republican_states:
            republican_electors += state["electors"]
            ImageDraw.floodfill(map, xy=state["location"],
                                value=state["color"])
            if state["name"] in biden_states:
                republican_states.remove(state["name"])
                republican_states.append("**"+state["name"]+"**")
                ImageDraw.floodfill(map, xy=state["location"],
                                    value=republican_flip_color)
    imgbytearr = io.BytesIO()
    map.save(imgbytearr, "png")
    imgbytearr.seek(0)
    if republican_electors > democratic_electors:
        winner = "The Republicans"
        swing = republican_electors - republican_electors_2020
    elif democratic_electors > republican_electors:
        winner = "The Democrats"
        swing = democratic_electors - democratic_electors_2020
    else:
        winner = "Nobody"
        swing = 0
    embed = embeds.twoembed("2024 Presidential Election", f"{winner} won the election!\n"
                                                          f"{winner} swung {str(swing)} electoral votes.\n"
                                                          f"If a state is flipped, it will be in bold.")
    embed.add_field(name="Republican Electoral Votes", value=str(republican_electors), inline=True)
    embed.add_field(name="Democratic Electoral Votes", value=str(democratic_electors), inline=True)
    republican_states_humanized = ""
    republican_state_count = 0
    for state in republican_states:
        if republican_state_count == 0:
            republican_states_humanized += str(state)
        else:
            republican_states_humanized += f", {str(state)}"
        republican_state_count += 1
    democratic_states_humanized = ""
    democratic_state_count = 0
    for state in democrat_states:
        if democratic_state_count == 0:
            democratic_states_humanized += str(state)
        else:
            democratic_states_humanized += f", {str(state)}"
        democratic_state_count += 1
    embed.add_field(name="Republican States", value=str(republican_states_humanized), inline=False)
    embed.add_field(name="Democratic States", value=str(democratic_states_humanized), inline=False)
    return {"embed": embed, "bytes": imgbytearr}
