from discord.ext import commands
from utils.logger import bot_logger

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        bot_logger.info('OK')
        await ctx.send('everything ok')

def setup(bot):
    bot.add_cog(Info(bot))
