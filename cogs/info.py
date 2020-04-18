import discord
from discord.ext import commands

import datetime


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
            status = ctx.author.status
            avatar_url = ctx.author.avatar_url

            embed_author = discord.Embed(title='Your info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
            ), footer=f'Requested by {ctx.author.name}')

            embed_author.set_author(
                name=user_name, url=discord.Embed.Empty, icon_url=avatar_url)

            embed_author.set_thumbnail(url=avatar_url)

            embed_author.add_field(
                name='UserName:', value=user_name, inline=True)
            embed_author.add_field(name='UserID:', value=user_id, inline=True)
            embed_author.add_field(
                name='UserTag:', value=user_name + user_discriminator, inline=True)

            if not user_name == display_name:
                embed_author.add_field(
                    name='Nickname:', value=display_name, inline=True)
            else:
                embed_author.add_field(
                    name='Nickname:', value='None', inline=True)

            embed_author.add_field(
                name='CreatedAt:', value=created_at, inline=True)
            embed_author.add_field(
                name='JoinedAt:', value=joined_at, inline=True)
            embed_author.add_field(name='Status:', value=status, inline=True)

            print(ctx.author.activity)

            activities = ctx.author.activities
            print(activities)

            await ctx.send(embed=embed_author)
            return

        embed_user = discord.Embed(title=f'{user.name}\'s info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
        ), footer=f'Requested by {ctx.author.name}')

        user_name = user.name
        user_id = user.id
        user_discriminator = user.discriminator
        is_bot = user.bot
        created_at = user.created_at
        display_name = user.display_name
        joined_at = user.joined_at
        status = user.status
        avatar_url = user.avatar_url

        embed_user.set_author(
            name=user_name, url=discord.Embed.Empty, icon_url=avatar_url)

        embed_user.set_thumbnail(url=avatar_url)

        embed_user.add_field(name='UserName:', value=user_name, inline=True)
        embed_user.add_field(name='UserID:', value=user_id, inline=True)
        embed_user.add_field(
            name='UserTag:', value=user_name + user_discriminator, inline=True)

        if not user_name == display_name:
            embed_user.add_field(
                name='Nickname:', value=display_name, inline=True)
        else:
            embed_user.add_field(name='Nickname:', value='None', inline=True)

        embed_user.add_field(name='Bot:', value=is_bot, inline=True)

        embed_user.add_field(
            name='CreatedAt:', value=created_at, inline=True)
        embed_user.add_field(
            name='JoinedAt:', value=joined_at, inline=True)
        embed_user.add_field(name='Status:', value=status, inline=True)

        print(user.activity)

        activities = ctx.author.activities
        print(activities)

        await ctx.send(embed=embed_user)


def setup(bot):
    bot.add_cog(Info(bot))
