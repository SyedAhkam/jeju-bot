from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import os
import datetime
import discord

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds


class Config(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set_mod_role', help='Set a role to be used as a ModRole.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_mod_role(self, ctx, role: commands.RoleConverter=None):
        if not role:
            await ctx.send('Please provide a role to be set as a ModRole.')
            return

        if role.name == '@everyone':
            await ctx.send('I highly discourage making everyone a Mod.')
            return

        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"mod_role": role.id}})    

        await ctx.send(f'Role ``{role.name}`` with ID: ``{role.id}`` has been set as a ModRole successfully.')

    @commands.command(name='set_modlog_channel', help='Set a channel to be used for ModLogs.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_modlog_channel(self, ctx, channel: commands.TextChannelConverter=None):
        if not channel:
            await ctx.send('Please provide a channel to set as a ModLogs Channel.')
            return
        
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"modlog_channel": channel.id}})

        await ctx.send(f'Channel ``{channel.name}`` with ID: ``{channel.id}`` has been set up as a ModLogs channel successfully.')

    @commands.command(name='set_venting_channel', help='Setup a venting channnel to vent anonymously')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_venting_channel(self, ctx, channel: commands.TextChannelConverter=None):
        if not channel:
            await ctx.send('Please provide a channel to be set as a venting channel.')
            return

        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {"$set": {"venting_channel": channel.id}})

        await ctx.send(f'Channel ``{channel.name}`` with ID: ``{channel.id}`` has been set up as a Venting channel successfully.')

    @commands.command(name='change_prefix', help='Change the bot\'s prefix.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def change_prefix(self, ctx, prefix=None):
        if not prefix:
            await ctx.send('Please specify a prefix.')
            return

        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"guild_prefix": prefix}})

        await ctx.send(f'Prefix set to ``{prefix}``')

    @commands.command(name='set_join_channel', help='Setup a channel for join logs.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_join_channel(self, ctx, channel: commands.TextChannelConverter=None):
        if not channel:
            await ctx.send('Please provide a channel to be set as a joinchannel.')
            return
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"join_channel": channel.id}})

        await ctx.send(f'Channel ``{channel.name}`` with ID: ``{channel.id}`` has been set up as a Join channel successfully.')

    @commands.command(name='set_leave_channel', help='Setup a channel for leave logs.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_join_channel(self, ctx, channel: commands.TextChannelConverter=None):
        if not channel:
            await ctx.send('Please provide a channel to be set as a leave channel.')
            return
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"leave_channel": channel.id}})

        await ctx.send(f'Channel ``{channel.name}`` with ID: ``{channel.id}`` has been set up as a leave channel successfully.')

    @commands.command(name='set_join_message', help='Setup a join message to be sent to your join channel everytime someone joins.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_join_message(self, ctx, *, join_message=None):
        if not join_message:
            await ctx.send('Please provide a message.')
            return

        guild_doc = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})

        if not 'join_channel' in guild_doc:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        if not guild_doc['join_channel']:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        #Save to db
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"join_message": join_message}})
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"join_message_set": True}})

        embed = discord.Embed(title='Join Message set to:', description=join_message, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        await ctx.send(embed=embed)

    @commands.command(name='set_leave_message', help='Setup a leave message to be sent to your leave channel everytime someone leaves.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def set_leave_message(self, ctx, *, leave_message=None):
        if not leave_message:
            await ctx.send('Please provide a message.')
            return

        guild_doc = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})

        if not 'leave_channel' in guild_doc:
            await ctx.send('Please setup a leave channel first using the command ``set_leave_channel``.')
            return
        
        if not guild_doc['leave_channel']:
            await ctx.send('Please setup a join channel first using the command ``set_leave_channel``.')
            return
        
        #Save to db
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"leave_message": leave_message}})
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"leave_message_set": True}})

        embed = discord.Embed(title='Leave Message set to:', description=leave_message, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        await ctx.send(embed=embed)
    
    @commands.command(name='test_join_message', help='Test the join message you set using ``set_join_message``.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def test_join_message(self, ctx):

        guild_doc = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})

        if not 'join_channel' in guild_doc:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        if not guild_doc['join_channel']:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        if not 'join_message' in guild_doc:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        if not guild_doc['join_message']:
            await ctx.send('Please setup a join channel first using the command ``set_join_channel``.')
            return
        
        join_channel = ctx.guild.get_channel(guild_doc['join_channel'])

        formatted_message = guild_doc['join_message']

        if '{user}' in formatted_message:
            formatted_message = formatted_message.replace('{user}', ctx.author.name)

        if '{user_mention}' in formatted_message:
            formatted_message = formatted_message.replace('{user_mention}', ctx.author.mention)
        
        if '{user_id}' in formatted_message:
            formatted_message = formatted_message.replace('{user_id}', str(ctx.author.id))
        
        if '{user_tag}' in formatted_message:
            formatted_message = formatted_message.replace('{user_tag}', f'{ctx.author.name}#{ctx.author.discriminator}')
        
        if '{server}' in formatted_message:
            formatted_message = formatted_message.replace('{server}', ctx.guild.name)
        
        if '{server_members}' in formatted_message:
            formatted_message = formatted_message.replace('{server_members}', len(ctx.guild.members))
        
        await join_channel.send(formatted_message)
    
    @commands.command(name='test_leave_message', help='Test the leave message you set using ``set_leave_message``.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def test_leave_message(self, ctx):

        guild_doc = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})

        if not 'leave_channel' in guild_doc:
            await ctx.send('Please setup a leave channel first using the command ``set_leave_channel``.')
            return
        
        if not guild_doc['leave_channel']:
            await ctx.send('Please setup a leave channel first using the command ``set_leave_channel``.')
            return
        
        if not 'leave_message' in guild_doc:
            await ctx.send('Please setup a leave channel first using the command ``set_leave_channel``.')
            return
        
        if not guild_doc['leave_message']:
            await ctx.send('Please setup a leave channel first using the command ``set_leave_channel``.')
            return
        
        
        leave_channel = ctx.guild.get_channel(guild_doc['leave_channel'])

        formatted_message = guild_doc['leave_message']

        if '{user}' in formatted_message:
            formatted_message = formatted_message.replace('{user}', ctx.author.name)

        if '{user_mention}' in formatted_message:
            formatted_message = formatted_message.replace('{user_mention}', ctx.author.mention)
        
        if '{user_id}' in formatted_message:
            formatted_message = formatted_message.replace('{user_id}', str(ctx.author.id))
        
        if '{user_tag}' in formatted_message:
            formatted_message = formatted_message.replace('{user_tag}', f'{ctx.author.name}#{ctx.author.discriminator}')
        
        if '{server}' in formatted_message:
            formatted_message = formatted_message.replace('{server}', ctx.guild.name)
        
        if '{server_members}' in formatted_message:
            formatted_message = formatted_message.replace('{server_members}', len(ctx.guild.members))
        
        await leave_channel.send(formatted_message)

    @commands.command(name='placeholders', help='See the list of placeholders Available for each command.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def placeholders(self, ctx):

        description = '''
        ``{user}`` gives the user's name.
        ``{user_mention}`` gives the user's tag as a mention.
        ``{user_id}`` gives the user's id.
        ``{user_tag}`` gives the user's tag.
        ``{server}`` gives the server's name.
        ``{server_members}`` gives the server's total members.
        '''
        
        embed = discord.Embed(title='Placeholders', description=description, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Config(bot))
