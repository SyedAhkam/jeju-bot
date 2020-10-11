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
            # BUG: may create more issues in the future
            if ctx.invoked_with in ['help', 'h']:
                return True
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True

    @commands.command(
        name='purge',
        aliases=['clear'],
        brief='Purges the specified number of messages.'
    )
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, messages: int):
        """**Purge the specified amount of messages**
        **Args**:
        - `messages`: Number of messages to delete.
        **Examples**: ```bash
        +purge 10
        +purge 50
        ```
        """
        await ctx.message.delete()

        deleted = await ctx.channel.purge(limit=messages)
        embed = normal_embed(
            ctx,
            title='Purged messages',
            description=f'Successfully purged {len(deleted)} messages.'
        )

        await ctx.send(embed=embed, delete_after=3)

    @commands.command(
        name='kick',
        brief='Kick a member out of the server.'
    )
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        """**Kick the specified member from the guild**
        **Args**:
        - `member`: The member to kick.
        - `reason`: The reason for kicking. This is optional.
        **Examples**: ```bash
        +kick 659094769607245845
        +kick @MEE6 cuz why not
        ```
        """

        if member == ctx.author:
            await ctx.send('You can\'t kick yourself.')
            return

        await member.kick(reason=reason)

        embed = normal_embed(
            ctx,
            title='Kicked',
            description=f'Successfully kicked `{member.name}`.'
        )
        await ctx.send(embed=embed)

    @commands.command(
        name='ban',
        brief='Ban a user from the server.'
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: commands.UserConverter, *, reason=None):
        """**Ban the specified user from the guild**
        **Args**:
        - `user`: The user to ban.
        - `reason`: The reason for banning. This is optional.
        **Examples**: ```bash
        +ban 659094769607245845
        +ban @MEE6 cuz why not
        ```
        """

        if user == ctx.author:
            await ctx.send('You can\'t ban yourself.')
            return

        await ctx.guild.ban(user, reason=reason)

        embed = normal_embed(
            ctx,
            title='Banned',
            description=f'Successfully banned `{user.name}`.'
        )
        await ctx.send(embed=embed)

    @commands.command(
        name='unban',
        brief='Unban a user from the server.'
    )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: commands.UserConverter, *, reason=None):
        """**Unban the specified user from the guild**
        **Args**:
        - `user`: The user to unban.
        - `reason`: The reason for unban. This is optional.
        **Examples**: ```bash
        +unban 659094769607245845
        +unban @MEE6 cuz people like you
        ```
        """

        await ctx.guild.unban(user, reason=reason)

        embed = normal_embed(
            ctx,
            title='Unbanned',
            description=f'Successfully unbanned `{user.name}`.'
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
