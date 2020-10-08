from discord.ext import commands
from utils.embeds import normal_embed

class Moderation(commands.Cog, name='moderation'):
    """All the moderation commands you'll ever need."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='purge',
        aliases=['clear'],
        brief='Purges the specified number of messages.'
    )
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        await ctx.message.delete()

        deleted = await ctx.channel.purge(limit=messages)
        embed = normal_embed(
            ctx,
            title='Purged messages',
            description=f'Successfully purged {len(deleted)} messages.'
        )

        await ctx.send(embed=embed, delete_after=3)

def setup(bot):
    bot.add_cog(Moderation(bot))
