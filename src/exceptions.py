from discord.ext import commands

class UserBlacklistedError(commands.CommandError):
    """A custom exception raised when a user is blacklisted."""
    def __init__(self, message=None, global_=False):
        super().__init__(message=message)
        self.global_ = global_

class ApiFetchError(commands.Cog):
    """A custom exception raised when a api fetch doesn't return a status code of 200"""
    def __init__(self, message=None, status=None):
        super().__init__(message=message)
        self.status = status
