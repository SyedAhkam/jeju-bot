from discord.ext import commands

class UserBlacklistedError(commands.CommandError):
    """A custom exception derived from CommandError"""
    def __init__(self, message=None, global_=False):
        super().__init__(message=message)
        self.global_ = global_
