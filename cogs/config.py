from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import os

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
    async def set_modlog_channel(self, ctx, channel: commands.TextChannelConverter=None):
        if not channel:
            await ctx.send('Please provide a channel to set as a ModLogs Channel.')
            return
        
        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"modlog_channel": channel.id}})
        await ctx.send(f'Channel ``{channel.name}`` with ID: ``{channel.id}`` has been set up as a ModLogs channel successfully.')

    @commands.command(name='change_prefix', help='Change the bot\'s prefix.')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix=None):
        if not prefix:
            await ctx.send('Please specify a prefix.')
            return

        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"guild_prefix": prefix}})

        await ctx.send(f'Prefix set to ``{prefix}``')

def setup(bot):
    bot.add_cog(Config(bot))
