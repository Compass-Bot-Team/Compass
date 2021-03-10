# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wavelink
import asyncio
from utils import embeds
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        self.bot.loop.create_task(self.run_lavalink())
        self.bot.loop.create_task(self.start_nodes())

    async def run_lavalink(self):
        lavalink_directory = f"{self.bot.directory}/lavalink"  # change this
        request = f"cd {lavalink_directory} & java -jar Lavalink.jar"
        await asyncio.create_subprocess_shell(request, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password=self.bot.config['password'],
                                              identifier='Compass',
                                              region='us_south')


    @commands.command(help="Connects to the current message author's voice chat.")
    async def connect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        try:
            await player.connect(ctx.author.voice.channel.id)
            await ctx.send(embed=embeds.twoembed(f"Connected to {ctx.author.voice.channel}!",
                                                 "Helo."))
        except Exception:
            await ctx.send(embed=embeds.failembed("Couldn't connect to a voice channel.",
                                                  "Try joining a voice channel."))

    @commands.command(help="Disconnects from the current message author's voice chat.  Only server moderators can use this, but if the message author is on their own, they can use this too!")
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(embed=embeds.failembed("Compass isn't connected!",
                                                         "You gotta connect it. bro."))
        members = len(ctx.author.voice.channel.members)
        if ctx.author.guild_permissions.move_members or members < 3:
            await player.disconnect()
            await ctx.send(embed=embeds.twoembed(f"Disconnected from {ctx.author.voice.channel}!",
                                                 "Cya."))
        else:
            return await ctx.send(embed=embeds.twoembed("Couldn't leave a voice channel.",
                                                        "You need perms (or you need to be the only one in VC!)"))

    async def length(self, length):
        seconds = round(length/1000)
        time = divmod(seconds, 60)
        return str(time).replace("(", "").replace(")", "").replace(", ", ":")

    @commands.command(help="Plays a song.")
    async def play(self, ctx, *, song):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{song}')
        if not tracks:
            return await ctx.send(embed=embeds.failembed(f'Could not find any songs. {self.bot.get_emoji(799142599927005184)}',
                                                         f'Try something else, I have no brain power sowwy.'))
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect)
        emoji = self.bot.get_emoji(799142822842335262)
        embed = embeds.twoembed(f'Added {str(tracks[0])} to the queue {emoji}',
                                f'[URL](https://www.youtube.com/watch?v={tracks[0].ytid})\n'
                                f'The length of this is {await self.length(tracks[0].length)}.')
        embed.set_thumbnail(url=tracks[0].thumb)
        await ctx.send(embed=embed)
        await player.play(tracks[0])

    @commands.command(help="Skips a song. Permissions are the same as connect.")
    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send(embed=embeds.failembed("YOU GOTTA be connected bro.",
                                                         "No connect = no skip = 1+1=2."))
        successembed = embeds.twoembed(f"Skipped the current song.", "Go nuts.")
        failembed = embeds.failembed("You don't have perms!", "You don't have perms to skip (you can also be the only one in the VC to skip.)")
        members = len(ctx.author.voice.channel.members)
        if ctx.author.guild_permissions.move_members or members < 3:
            await ctx.send(embed=successembed)
            await player.stop()
        else:
            await ctx.send(embed=failembed)


def setup(bot):
    bot.add_cog(Music(bot))
