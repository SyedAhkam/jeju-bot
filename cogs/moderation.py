# Imports
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv

import discord
import os
import datetime
import asyncio

# Load env variables
load_dotenv()

# Initialize the mongo_client
MONGO_URI = os.getenv('MONGODB_URI')
mongo_client = MongoClient(MONGO_URI)

db = mongo_client.jeju
guilds_collection = db.guilds

# A custom check for checking if user has mod role or not


def is_mod():
    def predicate(ctx):
        guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})
        mod_role = guild['mod_role']

        if not mod_role:
            ctx.channel.send(
                'Please setup a mod_role using the command ``set_mod_role``')
            return

        check = discord.utils.find(
            lambda r: r.id == mod_role, ctx.author.roles)
        if check:
            return True
    return commands.check(predicate)

# Main Cog Class


class Moderation(commands.Cog):

    # Initialize the class
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command(name='kick', help='Kicks a specified user.')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def kick(self, ctx, user: commands.MemberConverter = None, *, reason=None):

        if not user:
            await ctx.send('Please provide a user.')
            return

        if user == ctx.author:
            await ctx.send('You can\'t kick yourself.')
            return

        if user.id == ctx.guild.owner_id:
            await ctx.send('You can\'t kick the server owner.')
            return

        guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})
        modlog_channel = guild['modlog_channel']

        if not modlog_channel:
            await ctx.send('ModLogs channel not found, Set it up using ``set_modlog_channel``')

            await user.kick(reason=reason)
            await ctx.send(f'User {user.name} has been kicked successfully.')
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

        channel = ctx.bot.get_channel(modlog_channel)

        await user.kick(reason=reason)

        await channel.send(embed=kick_embed)
        await ctx.send(f'User {user.name} has been kicked successfully.')

    @commands.command(name='ban', help='Bans a specified user.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def ban(self, ctx, user: commands.MemberConverter = None, *, reason=None):

        if not user:
            await ctx.send('Please provide a user.')
            return

        if user == ctx.author:
            await ctx.send('You can\'t ban yourself.')
            return

        if user.id == ctx.guild.owner_id:
            await ctx.send('You can\'t ban the server owner.')
            return

        guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})
        modlog_channel = guild['modlog_channel']

        if not modlog_channel:
            await ctx.send('ModLogs channel not found, Set it up using ``set_modlog_channel``')

            await user.ban(reason=reason)
            await ctx.send(f'User {user.name} has been banned successfully.')
            return

        ban_embed = discord.Embed(title='Banned', description='A user have been Banned.',
                                  color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        ban_embed.set_author(
            name=user.name, url=discord.Embed.Empty, icon_url=user.avatar_url)

        ban_embed.add_field(
            name='Offender:', value=user.name + user.mention, inline=True)
        ban_embed.add_field(name='Reason:', value=reason, inline=True)
        ban_embed.add_field(name='Responsible moderator:',
                            value=ctx.author.name, inline=True)

        ban_embed.set_footer(text=f'UserID: {user.id}')

        channel = ctx.bot.get_channel(modlog_channel)

        await ctx.guild.ban(user, reason=reason)

        await channel.send(embed=ban_embed)
        await ctx.send(f'User {user.name} has been banned successfully.')

    @commands.command(name='unban', help='Unbans a specified user.')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def unban(self, ctx, user: commands.UserConverter = None):

        if not user:
            await ctx.send('Please provide a user.')
            return

        if user == ctx.author:
            await ctx.send('You can\'t unban yourself.')
            return

        if user.id == ctx.guild.owner_id:
            await ctx.send('You can\'t unban the server owner.')
            return

        guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})
        modlog_channel = guild['modlog_channel']

        if not modlog_channel:
            await ctx.send('ModLogs channel not found, Set it up using ``set_modlog_channel``')

            await ctx.guild.unban(user)
            await ctx.send(f'User {user.name} has been unbanned successfully.')
            return

        unban_embed = discord.Embed(title='Unbanned', description='A user have been Unbanned.',
                                    color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        unban_embed.set_author(
            name=user.name, url=discord.Embed.Empty, icon_url=user.avatar_url)

        unban_embed.add_field(
            name='Offender:', value=user.name + user.mention, inline=True)
        unban_embed.add_field(name='Responsible moderator:',
                              value=ctx.author.name, inline=True)

        unban_embed.set_footer(text=f'UserID: {user.id}')

        channel = ctx.bot.get_channel(modlog_channel)
        await channel.send(embed=unban_embed)

        await ctx.guild.unban(user)
        await ctx.send(f'User {user.name} has been unbanned successfully.')

    @commands.command(name='dm', help='DM\'s a specified user.')
    @commands.guild_only()
    @is_mod()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def dm(self, ctx, user: commands.MemberConverter = None, *, message=None):

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
    @commands.guild_only()
    @is_mod()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def say(self, ctx, *, message=None):

        if not message:
            await ctx.send('Please provide a message.')
            return

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='say_in_channel', help='Says Something given in a specified channel.')
    @commands.guild_only()
    @is_mod()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def say_in_channel(self, ctx, channel: commands.TextChannelConverter = None, *, message=None):

        if not channel:
            await ctx.send('Please provide a channel.')
            return

        if not message:
            await ctx.send('Please provide a message.')
            return

        await ctx.message.delete()
        await channel.send(message)

    @commands.command(name='purge', help='Purges the number of messages specified.')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def purge(self, ctx, messages: int = None):
        if not messages:
            await ctx.send('Please specify the number of messages to purge.')
            return

        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=messages)
        await ctx.send(f'Purged {len(deleted)} messages successfully.', delete_after=3)

    @commands.command(name='purge_unverified', help='Kick users who doesn\'t have the verified role.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def purge_unverified(self, ctx):
        await ctx.send('Would you like to DM them too?')
        answers = ['y', 'Y', 'yes', 'Yes']

        def check(msg):
            return msg.author == ctx.message.author and msg.channel == ctx.message.channel
        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=30.0)

            dm = bool(msg.content in answers)

            if dm:
                await ctx.send('What do you want me to DM them?')
                msg2 = await ctx.bot.wait_for('message', check=check, timeout=30.0)
                dm_message = msg2.content

            guild = guilds_collection.find_one(
                filter={"guild_id": ctx.guild.id})

            try:
                verified_role_id = guild['verified_role']
            except KeyError:
                await ctx.send('Please setup a verified role first using the command `set_verified_role`.')
                return

            if not verified_role_id:
                await ctx.send('Please setup a verified role first using the command `set_verified_role`.')
                return

            verified_role = ctx.guild.get_role(verified_role_id)

            progress = await ctx.send('Lemme calculate now...')
            bots = [x for x in ctx.guild.members if x.bot]
            total_members = ctx.guild.members
            unverified = [
                x for x in total_members if not verified_role in x.roles]

            if len(unverified) - len(bots) <= 0:
                await ctx.send('No unverified people detected.')
                return

            await progress.edit(content=f'So... from a total number of `{len(total_members)} members`, About `{len(unverified) - len(bots)}` members are unverfied excluding `{len(bots)}` bots..')

            await ctx.send('Do you still wanna continue? (Make sure i have `kick_members` permission)')
            msg3 = await ctx.bot.wait_for('message', check=check, timeout=30.0)
            if not msg3.content in answers:
                return

            progress2 = await ctx.send('Working on it, Please be patient.')

            for member in unverified:
                if member.bot:
                    continue
                if dm:
                    try:
                        await member.send(dm_message)
                    except discord.errors.Forbidden:
                        await progress2.edit(content=f'Can\'t DM this user: {member}, Skipping...')

                await member.kick(reason='Automatic action by jeju\'s `purge_unverified` command.')

            await progress2.edit(content='All done!')
            print(
                f'Purge unverified command has been used in: {ctx.guild.name} : {ctx.guild.id}')

        except asyncio.TimeoutError:
            await ctx.send('Timed out, Please try again later.')


# Define setup function to make this cog loadable
def setup(bot):
    bot.add_cog(Moderation(bot))
