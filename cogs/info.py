from discord.ext import commands


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping = round(ctx.bot.latency * 1000)
        await ctx.send(f'Pong!\n{ping}ms')

    @commands.command()
    async def user(self, ctx, user: commands.MemberConverter = None):

        if not user:
            user_name = ctx.author.name
            user_id = ctx.author.id
            user_discriminator = ctx.author.discriminator
            created_at = ctx.author.created_at
            display_name = ctx.author.display_name
            joined_at = ctx.author.joined_at

            if not user_name == display_name:
                await ctx.send(f'They have a nickname in this server: {display_name}')

            await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}\nCreatedAt: {created_at}\nJoinedAt: {joined_at}')

        user_name = user.name
        user_id = user.id
        user_discriminator = user.discriminator
        is_bot = user.bot
        created_at = user.created_at
        display_name = user.display_name
        joined_at = user.joined_at

        if not user_name == display_name:
                await ctx.send(f'They have a nickname in this server: {display_name}')

        if is_bot:
            await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}\nIt\'s a bot.\nCreatedAt: {created_at}\nJoinedAt: {joined_at}')
            return

        await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}\nCreatedAt: {created_at}\nJoinedAt: {joined_at}')


def setup(bot):
    bot.add_cog(Info(bot))
