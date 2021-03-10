import aiosqlite
from utils.useful_functions import wait_until
from discord.ext import commands


class Websocket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_and_update(self, event: str):
        await wait_until(self.bot)
        self.bot.not_allocated = False
        event = str(event.replace("_", " ")).upper()
        async with aiosqlite.connect("storage.db") as connection:
            async with connection.execute(f"""SELECT amount FROM Websocket WHERE name = "{event}";""") as cursor:
                info = (await cursor.fetchone())
            await connection.execute(f"""UPDATE Websocket SET amount = {int(info[0])+1} WHERE name = "{event}";""")
            await connection.commit()
        self.bot.not_allocated = True

    @commands.Cog.listener()
    async def on_connect(self):
        await self.load_and_update("on_connect")

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        await self.load_and_update("on_shard_connect")

    @commands.Cog.listener()
    async def on_disconnect(self):
        await self.load_and_update("on_disconnect")

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        await self.load_and_update("on_shard_disconnect")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_and_update("on_ready")

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        await self.load_and_update("on_shard_ready")

    @commands.Cog.listener()
    async def on_resumed(self):
        await self.load_and_update("on_resumed")

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        await self.load_and_update("on_shard_resumed")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        await self.load_and_update("on_error")

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        await self.load_and_update("on_socket_raw_receive")

    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload):
        await self.load_and_update("on_socket_raw_send")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        await self.load_and_update("on_typing")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.load_and_update("on_message")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.load_and_update("on_message_delete")

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        await self.load_and_update("on_bulk_message_delete")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        await self.load_and_update("on_raw_message_delete")

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        await self.load_and_update("on_raw_bulk_message_delete")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.load_and_update("on_message_edit")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        await self.load_and_update("on_raw_message_edit")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.load_and_update("on_reaction_add")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.load_and_update("on_raw_reaction_add")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.load_and_update("on_reaction_remove")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.load_and_update("on_raw_reaction_remove")

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        await self.load_and_update("on_reaction_clear")

    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload):
        await self.load_and_update("on_raw_reaction_clear")

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction):
        await self.load_and_update("on_reaction_clear_emoji")

    @commands.Cog.listener()
    async def on_raw_reaction_clear_emoji(self, payload):
        await self.load_and_update("on_raw_reaction_clear_emoji")

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel):
        await self.load_and_update("on_private_channel_delete")

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        await self.load_and_update("on_private_channel_create")

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        await self.load_and_update("on_private_channel_update")

    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, channel, last_pin):
        await self.load_and_update("on_private_channel_pins_update")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.load_and_update("on_guild_channel_delete")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.load_and_update("on_guild_channel_create")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        await self.load_and_update("on_guild_channel_update")

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        await self.load_and_update("on_guild_channel_pins_update")

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild):
        await self.load_and_update("on_guild_integrations_update")

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        await self.load_and_update("on_webhooks_update")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.load_and_update("on_member_join")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.load_and_update("on_member_remove")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.load_and_update("on_member_update")

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        await self.load_and_update("on_user_update")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.load_and_update("on_guild_join")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.load_and_update("on_guild_remove")

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        await self.load_and_update("on_guild_update")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.load_and_update("on_guild_role_create")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.load_and_update("on_guild_role_delete")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        await self.load_and_update("on_guild_role_update")

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        await self.load_and_update("on_guild_emojis_update")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        await self.load_and_update("on_guild_available")

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild):
        await self.load_and_update("on_guild_unavailable")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        await self.load_and_update("on_voice_state_update")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.load_and_update("on_member_ban")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await self.load_and_update("on_member_unban")

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.load_and_update("on_invite_create")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.load_and_update("on_invite_delete")

    @commands.Cog.listener()
    async def on_group_join(self, channel, user):
        await self.load_and_update("on_group_join")

    @commands.Cog.listener()
    async def on_group_remove(self, channel, user):
        await self.load_and_update("on_group_remove")

    @commands.Cog.listener()
    async def on_relationship_add(self, relationship):
        await self.load_and_update("on_relationship_add")

    @commands.Cog.listener()
    async def on_relationship_remove(self, relationship):
        await self.load_and_update("on_relationship_remove")

    @commands.Cog.listener()
    async def on_relationship_update(self, before, after):
        await self.load_and_update("on_relationship_update")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.load_and_update("on_command")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await self.load_and_update("on_command_completion")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.load_and_update("on_command_error")


def setup(bot):
    bot.add_cog(Websocket(bot))
