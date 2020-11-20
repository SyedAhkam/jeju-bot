from discord.ext import commands
from utils.embeds import normal_embed


class Info(commands.Cog, name='info'):
    """Some informational commands."""

    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            3,
            3,
            commands.BucketType.member
        )

    async def cog_check(self, ctx):
        bucket = self.cd_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True

    @commands.command(
        name='ping',
        aliases=['p', 'latency'],
        brief='Check the discord ws latency.'
    )
    async def ping(self, ctx):
        """Get the bot's latency in ms's.
        This could be referred to as the Discord WebSocket protocol latency.
        If you're experiencing high latency then probably something's up on the discord side. https://status.discord.com
        """
        latency = round(self.bot.latency * 1000)
        embed = normal_embed(
            ctx,
            title='Pong!',
            description=f"""Hello, I currently am experiencing a latency of ``{latency}ms``.
            If you\'re experiencing high latency then probably something\'s up on the discord side."""
        )
        await ctx.send(embed=embed)

    @commands.command(
        name='support',
        brief='Get an invite to the support server.'
    )
    async def support(self, ctx):
        invite_link = 'https://discord.gg/M4TtdBw'
        await ctx.send(f'**__My support server__**:\n{invite_link}')


def setup(bot):
    bot.add_cog(Info(bot))
