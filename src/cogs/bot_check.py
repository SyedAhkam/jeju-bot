from discord.ext import commands
from utils.db import is_document_exists
from exceptions import UserBlacklistedError


class BotCheck(commands.Cog):
    """A global check applied to every command"""

    def __init__(self, bot):
        self.bot = bot
        self.global_blacklist_collection = bot.db.global_blacklist

    async def bot_check(self, ctx):
        is_globally_blacklisted = await is_document_exists(self.global_blacklist_collection, ctx.author.id)
        if is_globally_blacklisted:
            raise UserBlacklistedError(
                f'{ctx.author} is blacklisted.', global_=True)
        return True


def setup(bot):
    bot.add_cog(BotCheck(bot))
