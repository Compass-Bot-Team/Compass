# MIT License
#
# Copyright (c) 2021 Compass
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import discord
import random

async def iourl(endpoint):
    return f"https://2b2t.io/api/{endpoint}"

async def devurl(endpoint):
    return f"https://api.2b2t.dev/{endpoint}"

async def acceptable(chance):
    if chance > 0:
        acceptable = [30, 35, 40, 45, 50]
    if chance > 20:
        acceptable = [35, 40, 45, 50, 60, 65]
    if chance > 30:
        acceptable = [40, 45, 50, 60, 65, 70]
    if chance > 50:
        acceptable = [45, 50, 60, 65, 70, 75]
    if chance > 60:
        acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100]
    if chance > 70:
        acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 125, 130, 140]
    if chance > 80:
        acceptable = [60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140, 145, 150, 155, 160]
    if chance > 90:
        acceptable = [80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140,
                      145, 150, 155, 160, 165, 175, 180]
    if chance > 95:
        acceptable = [90, 100, 105, 110, 115, 120, 125, 130, 140,
                      145, 150, 155, 160, 165, 175, 180, 185, 190, 195]
    return acceptable

async def classify(mph):
    global classification
    if mph > 0:
        classification = "Tropical Depression"
    if mph > 39:
        ts_or_ss = random.randint(0, 100)
        if ts_or_ss > 15:
            classification = "Tropical Storm"
        else:
            classification = "Subtropical Storm"
    if mph > 74:
        classification = "Hurricane"
    if mph > 110:
        classification = "Major Hurricane"
    return classification

async def poll_classic(message):
    await message.add_reaction('\U0001F7E9')
    await message.add_reaction('\U0001F7E8')
    await message.add_reaction('\U0001F7E5')
    await message.add_reaction("\U0001F7EA")
    await message.add_reaction("\u2754")


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

botinvite = 'https://discord.com/oauth2/authorize?client_id=769308147662979122&permissions=2147352567&scope=bot'

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"
         ]

bannedwebsites = ["https://www.pornhub.com",
                  "https://www.xvideos.com",
                  ]

# edit these as you would like to
valids = [721029142602056328,
          720330422726164500,
          574984194024013825,
          375461705032925184,
          210473676339019776,
          210958048691224576,
          217044793807601664]

memevalids = [721029142602056328,
              720330422726164500,
              574984194024013825,
              375461705032925184,
              210473676339019776,
              210958048691224576,
              217044793807601664,
              358522455507206145]
# ok don't edit anything underneath this thanks

usstates = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
            "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
            "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
            "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
            "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
            "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
            "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
            "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
            "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga",
            "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md",
            "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj",
            "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc",
            "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy",
            "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
            "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois",
            "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland",
            "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana",
            "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york",
            "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
            "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah",
            "vermont", "virginia", "washington", "west virginia", "wisconsin", "wyoming"]

blacklistedusers = []

numbers = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
           'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One',
           'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six', 'Twenty-Seven', 'Twenty-Eight',
           'Twenty-Nine', 'Thirty', 'Thirty-One', 'Thirty-Two', 'Thirty-Three', 'Thirty-Four', 'Thirty-Five',
           'Thirty-Six',
           'Thirty-Seven', 'Thirty-Eight', 'Thirty-Nine', 'Fourty', 'Fourty-One', 'Fourty-Two', 'Fourty-Three',
           'Fourty-Four',
           'Fourty-Five', 'Fourty-Six', 'Fourty-Seven', 'Fourty-Eight', 'Fourty-Nine', 'Fifty', 'Fifty-One',
           'Fifty-Two',
           'Fifty-Three', 'Fifty-Four', 'Fifty-Five']
_2026hurricanelist = ["Arthur", "Bertha", "Cristobal", "Dolly", "Edouard", "Fay", "Gonzalo", "Hanna", "Isaias",
                      "Josephine", "Kyle", "Marco", "Nana", "Omar", "Paulette", "Rene", "Sally", "Teddy", "Vicky", "Wilfred"]
_2021hurricanelist = ["Ana", "Bill", "Claudette", "Danny", "Elsa", "Fred", "Grace", "Henri", "Ida", "Julian", "Kate", "Larry", "Mindy", "Nicholas", "Odette", "Peter", "Rose", "Sam", "Teresa", "Victor", "Wanda"]
_2022hurricanelist = ["Alex", "Bonnie", "Colin", "Danielle", "Earl", "Fiona", "Gaston", "Hermine", "Ian", "Julia", "Karl", "Lisa", "Martin", "Nicole", "Owen", "Paula", "Richard", "Shary", "Tobias", "Virginie", "Walter"]
_2023hurricanelist = ["Arlene", "Bret", "Cindy", "Don", "Emily", "Franklin", "Gert", "Harold", "Idalia", "Jose", "Katia", "Lee", "Margot", "Nigel", "Ophelia", "Philippe", "Rina", "Sean", "Tammy", "Vince", "Whitney"]
_2024hurricanelist = ["Alberto", "Beryl", "Chris", "Debby", "Ernesto", "Francine", "Gordon", "Helene", "Isaac", "Joyce", "Kirk", "Leslie", "Milton", "Nadine", "Oscar", "Patty", "Rafael", "Sara", "Tony", "Valerie", "William"]
_2025hurricanelist = ["Andrea", "Barry", "Chantal", "Erin", "Fernand", "Gabrielle", "Humberto", "Imelda", "Jerry", "Karen", "Lorenzo", "Melissa", "Nestor", "Olga", "Pablo", "Rebekah", "Sebastien", "Tanya", "Van", "Wendy"]
greekhurricanelist = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda",
                      "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]


def helpembed(header, title1, text1, title2, text2, title3, text3, title4, text4, title5, text5, title6, text6, footer):
    embed_var = discord.Embed(colour=0x202225)
    embed_var.set_author(name=str(header))
    embed_var.add_field(name=str(title1), value=str(text1), inline=True)
    embed_var.add_field(name=str(title2), value=str(text2), inline=True)
    embed_var.add_field(name=str(title3), value=str(text3), inline=True)
    embed_var.add_field(name=str(title4), value=str(text4), inline=True)
    embed_var.add_field(name=str(title5), value=str(text5), inline=True)
    embed_var.add_field(name=str(title6), value=str(text6), inline=True)
    embed_var.set_footer(text=str(footer))
    return embed_var


def mainembed(header, title1, text1):
    embed_var = discord.Embed(colour=0x202225, title=str(header))
    embed_var.add_field(name=str(title1), value=str(text1), inline=True)
    return embed_var

def add_field(embed, title1, text1, inline1):
    embed_var = embed
    embed_var.add_field(name=title1, value=text1, inline=inline1)
    return embed_var

def twoembed(title1, text1):
    embed_var = discord.Embed(colour=0x202225, title=str(title1), description=str(text1))
    return embed_var

def imgembed(title, url):
    embed_var = discord.Embed(colour=0x202225, url=url, title=str(title))
    embed_var.set_image(url=url)
    return embed_var


def helptwoembed(pagenum, title1, text1):
    embed_var = discord.Embed(colour=0x202225, title=str(title1), description=str(text1))
    embed_var.set_footer(text=f"Page {str(pagenum)}")
    return embed_var


def successembed(header, title1, text1):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(0, 209, 24), title=str(header))
    embed_var.add_field(name=str(title1), value=str(text1), inline=True)
    return embed_var


def failembed(header, title1, text1):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title=str(header))
    embed_var.add_field(name=str(title1), value=str(text1), inline=True)
    return embed_var

def newfailembed(header, text):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title=str(header),
                              description=str(text))
    return embed_var


def command_disabled(ctx):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title="Command Disabled")
    embed_var.add_field(name=f"{ctx.message.author}, this command is disabled.",
                        value="It'll be enabled later once it's done.", inline=True)
    return embed_var


def you_cant_use_this():
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title="You can't use this!")
    embed_var.add_field(name="You can't use this command.",
                        value="Only the devs can!", inline=True)


def blacklisted(ctx):
    embed_var = discord.Embed(colour=discord.Colour.from_rgb(211, 0, 0), title="You can't use this!")
    embed_var.add_field(name=f"{ctx.message.author}, you're blacklisted.",
                        value="You actually got blacklisted from this command wtf?", inline=True)
    return embed_var


def walletembed(title, embedtext, embedval1, embedtext2, embedval3):
    embed_var = discord.Embed(colour=0x202225, title=str(title))
    embed_var.add_field(name=str(embedtext), value=str(embedval1), inline=True)
    embed_var.add_field(name=str(embedtext2), value=str(embedval3), inline=True)
    return embed_var


def workembed(title, text1, text2):
    embed_var = discord.Embed(colour=0x202225, title=str(title))
    embed_var.add_field(name=str(text1), value=str(text2))
    return embed_var

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


def dtog(id):
    if id == 721029142602056328:
        return True
    else:
        return False


def embedcolor():
    return 0x202225

async def checkfail(server):
    checkfail = newfailembed(f"You aren't in {server}!",
                             "Try harder.")
    return checkfail