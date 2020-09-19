from discord.ext import commands
from utils.logger import bot_logger
from utils.embeds import normal_embed

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping',
        aliases=['p', 'latency'],
        brief='Check the discord ws latency.'
    )
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = normal_embed(
            ctx,
            title='Pong!',
            description=f"""Hello, I currently am experiencing a latency of ``{latency}ms``.
            If you\'re experiencing high latency then probably something\'s up on the discord side."""
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
