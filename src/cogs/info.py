from discord.ext import commands
from utils.logger import bot_logger

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(enabled=True, ignore_extra=False)
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def test(self, ctx, argument1: int, argument2):
        bot_logger.info('OK')
        await ctx.send('everything ok')

def setup(bot):
    bot.add_cog(Info(bot))
