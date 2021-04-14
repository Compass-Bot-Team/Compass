from utils import embeds
from launcher import source
from discord.ext import commands


class NewBotHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        returned = command.qualified_name
        if command.aliases:
            for alias in command.aliases:
                returned += f"/{alias}"
        return returned

    async def send_command_help(self, command):
        channel = self.get_destination()
        async with channel.typing():
            title = self.get_command_signature(command)
            if command.signature:
                title += f" {command.signature}"
            embed = embeds.twoembed(f"``{title}``", command.help)
            embed.url = await source(command.qualified_name)
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        channel = self.get_destination()
        async with channel.typing():
            title = self.get_command_signature(group)
            if group.signature:
                title += f" {group.signature}"
            embed = embeds.twoembed(f"``{title}``", group.short_doc)
            embed.url = await source(group.qualified_name)
            subcommand_count = 0
            subcommands = ""
            if group.commands:
                for subcommand in group.commands:
                    if subcommand_count != 0: subcommands += ", "
                    subcommands += f"``{subcommand}``"
                    subcommand_count += 1
                embed.add_field(name="Subcommands", value=subcommands)
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        channel = self.get_destination()
        embed = embeds.twoembed(f"``{cog.qualified_name}``", cog.description)
        await channel.send(embed=embed)

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        embed = embeds.twoembed(f"NewBot help!", f"The used prefix was {self.clean_prefix}.")
        async with channel.typing():
            for cog, commands in mapping.items():
                filtered = await self.filter_commands(commands, sort=True)
                command_signatures = [self.get_command_signature(c) for c in filtered]
                command_count = 0
                commands_registered = ""
                if command_signatures:
                    for command in command_signatures:
                        if command_count == 0:
                            commands_registered += f"``{command}``"
                        else:
                            commands_registered += f", ``{command}``"
                        command_count += 1
                    cog_name = getattr(cog, "qualified_name", "Other")
                    embed.add_field(name=cog_name, value=commands_registered, inline=False)
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = NewBotHelp(command_attrs={'help': "Posts this message."})


def setup(bot):
    bot.add_cog(Help(bot))