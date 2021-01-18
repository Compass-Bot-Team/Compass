import asyncio
import os
import subprocess
import logging
import yaml
import time
from datetime import datetime
from databases import asqlite

baselogger = logging.getLogger(__name__)
logging.basicConfig(format=f"[{datetime.utcnow()} %(name)s %(levelname)s] %(message)s", level=logging.INFO)

def shell(command):
    return subprocess.run(f"cd {your_repo} & {command}", shell=True)

your_repo = str(os.getcwd())
baselogger.info(f"Working repository for config setup: " + your_repo)
baselogger.info(f"Database folder for config setup: {your_repo}\databases")
db_folder = f"{your_repo}\databases"

baselogger.info("Installing relevant Python packages.")
shell("pip3 install -U -r requirements.txt")

if not os.path.exists(your_repo+r"\image.png"):
    open(your_repo+r"\image.png", "w+")
    baselogger.info(f"No image.png file found in {your_repo}, created an image.png file for image cache.")
else:
    baselogger.info(f"image.png file found in {your_repo}, skipping this step.")

if not os.path.exists(db_folder+r"\quotes.txt"):
    open(db_folder+r"\quotes.txt", "w+")
    baselogger.info(f"No quotes.txt file found in {db_folder}, created an quotes.txt file in {db_folder} for quotes storage.")
else:
    baselogger.info(f"quotes.txt file found in {db_folder}, skipping this step.")

if not os.path.exists(db_folder+r"\8ballresponses.db"):
    async def create_8ball_db():
        async with asqlite.connect(db_folder+r"\8ballresponses.db") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE ballresponses (response)''')
                await conn.commit()
    asyncio.run(create_8ball_db())
    baselogger.info(f"No 8ballresponses.db file found in {db_folder}, created an 8ballresponses.db file in {db_folder} for 8ballresponses storage.")
else:
    baselogger.info(f"8ballresponses.db file found in {db_folder}, skipping this step.")

if not os.path.exists(db_folder+r"\eatresponses.db"):
    async def create_eatresponses_db():
        async with asqlite.connect(db_folder+r"\eatresponses.db") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE eatresponses (response)''')
                await conn.commit()
    asyncio.run(create_eatresponses_db())
    baselogger.info(f"No eatresponses.db file found in {db_folder}, created an eatresponses.db file in {db_folder} for eat response storage.")
else:
    baselogger.info(f"eatresponses.db file found in {db_folder}, skipping this step.")

if not os.path.exists(db_folder+r"\memes.db"):
    async def create_memes_db():
        async with asqlite.connect(db_folder+r"\memes.db") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE Memes (link)''')
                await conn.commit()
    asyncio.run(create_memes_db())
    baselogger.info(f"No memes.db file found in {db_folder}, created an memes.db file in {db_folder} for memes storage.")
else:
    baselogger.info(f"memes.db file found in {db_folder}, skipping this step.")

if not os.path.exists(db_folder+r"\prefixes.json"):
    baselogger.info(f"No prefixes.json file found in {db_folder}.")
    print("What is your Server ID?")
    server_id = input()
    print("What is your designated prefix?")
    prefix = input()
    with open(db_folder+r"\prefixes.json", "w+") as g:
        g.write("{" + f'"{str(server_id)}":' + '{' + f'"prefix": "{prefix}"' + "}}")
else:
    baselogger.info(f"prefixes.json file found in {db_folder}, skipping this step. If you want to edit the file using this file please delete prefixes.json")

if not os.path.exists(your_repo+r"\config.yml"):
    baselogger.info(f"No config.yml file found in {your_repo}. Initializing config menu...")
    time.sleep(1)
    print("What is your bot password?")
    password = input()
    print("What is the idea of the owner(s) of the bot instance?\n"
          "Use a space to split owner IDs")
    owners = list(str(input()).replace(",", "").split(" "))
    print("What is your MongoDB server url?")
    mongodbserver = input()
    print("What is your token?")
    token = input()
    print("What is your open weather map api key?")
    weather_key = input()
    print("What is your ksoftsi api key?")
    ksoftsi_key = input()
    print("What is your google api key?")
    google_key = input()
    print("What is your hypixel api key?")
    hypixel_key = input()
    print("What is your Steam api key?")
    steam_key = input()
    print("What is your GitHub token? (preferably give it every permission)")
    github_token = input()
    print("What is your NASA api key?")
    nasa_key = input()
    print("What is your OMDB api key?")
    omdb_key = input()
    print("What is your SR api key?")
    sra_key = input()
    print("What is your Reddit client secret?")
    client_secret = input()
    print("What is your Reddit client ID?")
    client_id = input()
    print("What is your Reddit user agent?")
    user_agent = input()
    data = {"developers": [721029142602056328],
            "owners": owners,
            "password": str(password),
            "mongodbserver": str(mongodbserver),
            "token": str(token),
            "weatherapikey": str(weather_key),
            "ksoftsikey": str(ksoftsi_key),
            "googleapikey": str(google_key),
            "hypixelapikey": str(hypixel_key),
            "steamapikey": str(steam_key),
            "githubkey": str(github_token),
            "nasakey": str(nasa_key),
            "omdbkey": str(omdb_key),
            "srakey": str(sra_key),
            "redditauth": [str(client_secret), str(client_id), str(user_agent)]}
    with open(your_repo+"\config.yml", "w+") as c:
        yaml.dump(data, c)
else:
    baselogger.info(f"config.yml file found in {your_repo}, skipping this step. If you want to edit the file using this file please delete config.yml")