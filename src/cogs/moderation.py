from discord.ext import commands
from utils.embeds import normal_embed


class Moderation(commands.Cog, name='moderation'):
    """All the moderation commands you'll ever need."""

    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            3,
            2,
            commands.BucketType.member
        )

    async def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage()

        bucket = self.cd_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(self.cd_mapping, retry_after)
        return True

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
