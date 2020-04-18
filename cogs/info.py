import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping = round(ctx.bot.latency * 1000)
        await ctx.send(f'Pong!\n{ping}ms')

    @commands.command()
    async def user(self, ctx, user: commands.MemberConverter=None):

        if not user:
            user_name = ctx.author.name
            user_id = ctx.author.id
            user_discriminator = ctx.author.discriminator
            await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}')

        user_name = user.name
        user_id = user.id
        user_discriminator = user.discriminator
        is_bot = user.bot

        if is_bot:
            await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}\nIt\'s a bot.')
            return

        await ctx.send(f'UserName: {user_name}\nUserID: {user_id}\nUserDiscriminator: {user_discriminator}')

def setup(bot):
    bot.add_cog(Info(bot))