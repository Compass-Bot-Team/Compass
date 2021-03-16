from discord.ext import commands


class MissingSubcommand(Exception):
    """No subcommand found!"""


commands.MissingSubcommand = MissingSubcommand


class ImageManipulationError(Exception):
    """Base class for Image Manipulation errors."""


class ImageExceedsLimit(ImageManipulationError):
    """Exception raised when an image exceeds the limit the bot is willing to handle"""


class Blacklisted(Exception):
    """Exception raised when a user is blacklisted, but is trying to use the bot."""
