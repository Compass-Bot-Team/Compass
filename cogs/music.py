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

import objectfile
import yaml
import wavelink
import sr_api
from discord.ext import commands

config = yaml.safe_load(open("config.yml"))
client = sr_api.Client(config['srakey'])
music_commands = ['connect', 'skip', 'disconnect', 'play']

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        try:
            await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                                  port=2333,
                                                  rest_uri='http://127.0.0.1:2333',
                                                  password=config['password'],
                                                  identifier='Compass',
                                                  region='us_south')
        except Exception:
            return

    @commands.command(help="Connects to the current message author's voice chat.")
    async def connect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try:
            await player.connect(ctx.author.voice.channel.id)
            await ctx.send(embed=objectfile.twoembed(f"Connected to {ctx.author.voice.channel}!",
                                                     "Helo."))
        except Exception:
            await ctx.send(embed=objectfile.newfailembed("Couldn't connect to a voice channel.",
                                                         "Try joining a voice channel."))

    @commands.command(help="Disconnects from the current message author's voice chat. "
                           "Only server moderators can use this, but if the message author "
                           "is on their own, they can use this too!")
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(embed=objectfile.newfailembed("Compass isn't connected!",
                                                                "You gotta connect it. bro."))
        members = len(ctx.author.voice.channel.members)
        if ctx.author.guild_permissions.move_members or members < 3:
            try:
                await player.disconnect()
                await ctx.send(embed=objectfile.twoembed(f"Disconnected from {ctx.author.voice.channel}!",
                                                         "Cya."))
            except Exception:
                return await ctx.send(embed=objectfile.newfailembed("Couldn't leave a voice channel.",
                                                                    "Try joining a voice channel."))
        else:
            return await ctx.send(embed=objectfile.newfailembed("Couldn't leave a voice channel.",
                                                                "You need perms (or you need to be the only one in VC!)"))

    async def length(self, length):
        seconds = round(length/1000)
        time = divmod(seconds, 60)
        return str(time).replace("(", "").replace(")", "").replace(", ", ":")


    @commands.command(help="Plays a song.")
    async def play(self, ctx, *, song):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{song}')
        if not tracks:
            return await ctx.send(embed=objectfile.newfailembed(f'Could not find any songs. {self.bot.get_emoji(799142599927005184)}',
                                                                'Try something else, I have no brain power sowwy.'))
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect)
        emoji = self.bot.get_emoji(799142822842335262)
        embed = objectfile.twoembed(f'Added {str(tracks[0])} to the queue {emoji}',
                                    f'[URL](https://www.youtube.com/watch?v={tracks[0].ytid})\n'
                                    f'The length of this is {await self.length(tracks[0].length)}.')
        embed.set_thumbnail(url=tracks[0].thumb)
        await ctx.send(embed=embed)
        await player.play(tracks[0])

    @commands.command(help="Skips a song. Permissions are the same as connect.")
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(embed=objectfile.newfailembed("YOU GOTTA be connected bro.",
                                                                "No connect = no skip = 1+1=2."))
        successembed = objectfile.twoembed(f"Skipped the current song.",
                                           "Go nuts.")
        failembed = objectfile.newfailembed("You don't have perms!",
                                            "You don't have perms to skip (you can also be the only one in the VC to skip.)")
        members = len(ctx.author.voice.channel.members)
        if ctx.author.guild_permissions.move_members or members < 3:
            await ctx.send(embed=successembed)
            await player.stop()
        else:
            await ctx.send(embed=failembed)


def setup(bot):
    bot.add_cog(Music(bot))
