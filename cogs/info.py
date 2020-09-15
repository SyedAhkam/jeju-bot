from discord.ext import commands

import logging

logger = logging.getLogger('bot')

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        logger.info('OK')
        self.bot.logger.info('aaaaaaaa')
        await ctx.send('everything ok')

def setup(bot):
    bot.add_cog(Info(bot))
