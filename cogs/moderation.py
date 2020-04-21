import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
import datetime

load_dotenv()
MODLOGS = int(os.getenv('MODLOGS_CHANNEL'))
SAYROLE = int(os.getenv('SAY_ROLE_ID'))
DMROLE = int(os.getenv('DM_ROLE_ID'))


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='Kicks a specified user.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: commands.MemberConverter=None, *, reason=None):

        if not user:
            await ctx.send('Please provide a user.')
            return

        if not reason:
            await ctx.send('Please provide a reason.')
            return


        kick_embed = discord.Embed(title='Kicked', description='A user have been kicked.',
                                   color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        kick_embed.set_author(
            name=user.name, url=discord.Embed.Empty, icon_url=user.avatar_url)

        kick_embed.add_field(
            name='Offender:', value=user.name + user.mention, inline=True)
        kick_embed.add_field(name='Reason:', value=reason, inline=True)
        kick_embed.add_field(name='Responsible moderator:',
                             value=ctx.author.name, inline=True)

        kick_embed.set_footer(text=f'UserID: {user.id}')

        channel = ctx.bot.get_channel(MODLOGS)
        await channel.send(embed=kick_embed)

        await user.kick(reason=reason)
        await ctx.send(f'User {user.name} has been kicked successfully.')

    @commands.command(name='ban', help='Bans a specified user.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, id: int, *, reason):

        if not id:
            await ctx.send('Please provide a user\'s id.')
            return

        if not reason:
            await ctx.send('Please provide a reason.')
            return

        user = ctx.bot.get_user(id)

        ban_embed = discord.Embed(title='Banned', description='A user have been Banned.',
                                  color=0xFFFFFF, timestamp=datetime.datetime.utcnow(), footer=user.id)

        ban_embed.set_author(
            name=user.name, url=discord.Embed.Empty, icon_url=user.avatar_url)

        ban_embed.add_field(
            name='Offender:', value=user.name + user.mention, inline=True)
        ban_embed.add_field(name='Reason:', value=reason, inline=True)
        ban_embed.add_field(name='Responsible moderator:',
                            value=ctx.author.name, inline=True)

        ban_embed.set_footer(text=f'UserID: {user.id}')

        channel = ctx.bot.get_channel(MODLOGS)
        await channel.send(embed=ban_embed)

        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'User {user.name} has been banned successfully.')

    @commands.command(name='unban', help='Unbans a specified user.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):

        if not id:
            await ctx.send('Please provide a user\'s id.')
            return

        user = ctx.bot.get_user(id)

        unban_embed = discord.Embed(title='Unbanned', description='A user have been Unbanned.',
                                    color=0xFFFFFF, timestamp=datetime.datetime.utcnow(), footer=user.id)

        unban_embed.set_author(
            name=user.name, url=discord.Embed.Empty, icon_url=user.avatar_url)

        unban_embed.add_field(
            name='Offender:', value=user.name + user.mention, inline=True)
        unban_embed.add_field(name='Responsible moderator:',
                              value=ctx.author.name, inline=True)

        unban_embed.set_footer(text=f'UserID: {user.id}')

        channel = ctx.bot.get_channel(MODLOGS)
        await channel.send(embed=unban_embed)

        await ctx.guild.unban(user)
        await ctx.send(f'User {user.name} has been unbanned successfully.')

    @commands.command(name='dm', help='DM\'s a specified user.')
    @commands.has_role(DMROLE)
    async def dm(self, ctx, user: commands.MemberConverter=None, *, message=None):

        if not user:
            await ctx.send('Please provide a user.')
            return

        if not message:
            await ctx.send('Please provide a message.')
            return

        await ctx.message.delete()
        await user.create_dm()
        await user.dm_channel.send(message)

    @commands.command(name='say', help='Says Something given.')
    @commands.has_role(SAYROLE)
    async def say(self, ctx, *, message=None):

        if not message:
            await ctx.send('Please provide a message.')
            return

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='say_in_channel', help='Says Something given in a specified channel.')
    @commands.has_role(SAYROLE)
    async def say_in_channel(self, ctx, channel: commands.TextChannelConverter=None, *, message=None):

        if not channel:
            await ctx.send('Please provide a channel.')
            return

        if not message:
            await ctx.send('Please provide a message.')
            return
        
        await ctx.message.delete()
        await channel.send(message)

    @commands.command(name='purge', help='Purges the number of messages specified.')
    async def purge(self, ctx, messages: int=None):
        if not messages:
            await ctx.send('Please specify the number of messages to purge.')
            return
        
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=messages)
        await ctx.send(f'Purged {len(deleted)} messages successfully.', delete_after=3)

def setup(bot):
    bot.add_cog(Moderation(bot))
