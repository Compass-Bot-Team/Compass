## Setting up Compass
Setting up the bot is difficult if you don't know what you're doing which is why I recommend you just invite the instance of the bot I run myself [here.](https://discord.com/oauth2/authorize?client_id=769308147662979122&permissions=2147352567&scope=bot) However, if you still want to set up the bot on your own machine, there isn't anything I can do to stop you.

## Requirements
Python requirements;
* Python 3.7+ (preferably Python 3.8.*)
* cd to the working directory, and type ``pip install -r requirements.txt``. You can use pip or pip3
* ``pip install PyNaCl`` or ``pip3 install PyNaCl``, for voice support. **Do not use Heroku or repl.it for this bot, if you did not get the memo already.**
* JDK 13, you can get JDK 13 [here](https://openjdk.java.net/projects/jdk/13/). If you want to link a good tutorial make a PR
* Lavalink, you can get lavalink [here](https://github.com/Frederikam/Lavalink). All you have to do is install lavalink into any directory on the same machine on the bot in it's own folder. It can also be in a subfolder
* Create a file named image.png in the main directory for image cache

## Lavalink setup guide
In your working directory for lavalink which you have installed before hopefully, create a file called application.yml.
The application.yml file the bot uses (with the password removed) can be found [here.](https://github.com/Compass-Bot-Team/Compass/blob/main/application.yml) Just copy and paste the file into your Lavalink directory. Cd to the directory and run ``java -jar Lavalink.jar``. It is recommended you set up a process manager.

## config.yml setup guide
Create a file called config.yml. Put this in your bot directory (not in your cogs directory.) Here's the recommended structure for what this should look like;
```yml
developers:
  - 721029142602056328 # PLEASE keep this as it is, I would like credit for my project. However I can't stop you from doing anything.
password: # Bot password for things like lavalink nodes and pastebin
mongodbserver: # Mongo DB server url, this isn't required for anything so just ignore this but it's recommended you put this in
token: # The bot token
# Keys
weatherapikey: # Open weather map api key, go to their website at https://openweathermap.org/
ksoftsikey: # Ksoftsi api key, this isn't required for anything so just ignore this but it's recommended you put this in
googleapikey: # Google api key for the google command, you can get an api key [here](https://developers.google.com/custom-search/v1/overview)
hypixelapikey: # Hypixel api key, go on the hypixel official minecraft server on java edition and type /api to get your api key
steamapikey: # leave this blank
githubkey: # Github token for any bot accounts you want (keep in mind you have to go to the errors cog and remove the relevant github issues lines) 
nasakey: # NASA api key, go to https://api.nasa.gov/ and get an api key
omdbkey: # Omdb key for IMDB searches, get an api key at https://www.omdbapi.com/apikey.aspx
srakey: # leave this blank (go to apis.py and take out the field yourself)
# Reddit
redditauth: # Go to the official async praw docs for this one (https://asyncpraw.readthedocs.io/)
  - # Reddit client secret
  - # Reddit client id
  - # Reddit user agent
# GitHub
repos:
  - botrepo: "Compass" # keep this the same
  - websiterepo: "Compass-Bot-Team.github.io" # keep this the same
```