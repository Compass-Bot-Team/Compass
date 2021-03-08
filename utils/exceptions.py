class ImageManipulationError(Exception):
    """Base class for Image Manipulation errors."""


class ImageExceedsLimit(ImageManipulationError):
    """Exception raised when an image exceeds the limit the bot is willing to handle"""
