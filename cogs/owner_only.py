# Imports
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import os

# Load env variables
load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

# Initialize the mongo_client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju

guilds_collection = db.guilds
bot_collection = db.bot

# Main Cog Class
class OwnerOnly(commands.Cog):

    # Initialize the class
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command(name='load', help='Loads a specified category.')
    @commands.is_owner()
    async def load(self, ctx, extension):
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded Successfully.')

    @commands.command(name='unload', help='Unloads a specified category.')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded Successfully.')

    @commands.command(name='reload', help='Reloads a specified category.')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} reloaded Successfully.')

    @commands.command(name='eval', help='Evaluate a piece of code.')
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        await ctx.send(eval(code) + '\nDone')

    @commands.command(name='load_guilds', help='Load the guilds in the database.')
    @commands.is_owner()
    async def load_guilds(self, ctx):

        msg = await ctx.send('In progress...')

        already_in_db = 0
        added_in_db = 0

        for guild in ctx.bot.guilds:

            exists = guilds_collection.count_documents(filter={"guild_id": guild.id}) > 0
            if exists:
                already_in_db += 1
            else:
                post = {
                    "guild_id": guild.id,
                    "guild_name": guild.name,
                    "guild_region": guild.region,
                    "guild_icon": guild.icon,
                    "guild_owner_id": guild.owner_id,
                    "members": len(guild.members),
                    "guild_description": guild.description,
                    "guild_verification": guild.verification_level,
                    "guild_features": guild.features
                }
                guilds_collection.insert_one(post)
                added_in_db += 1

        total_guilds = guilds_collection.count_documents(filter={})

        if already_in_db > 0 and added_in_db == 0:
            await msg.edit(content=f'{already_in_db} guild(s) were already in db and no new guild(s) detected.\nTotalGuilds in db: {total_guilds}')

        elif already_in_db == 0 and added_in_db > 0:
            await msg.edit(content=f'{added_in_db} new guild(s) were detected and have been loaded successfully.\nTotalGuilds in db: {total_guilds}')

        elif already_in_db > 0 and added_in_db > 0:
            await msg.edit(content=f'{already_in_db} guild(s) were already in db and {added_in_db} new guild(s) were detected and have been loaded successfully.\nTotalGuilds in db: {total_guilds}')

        else:
            await msg.edit(content=f'No guild(s) were detected or an error occured.\nTotalGuilds in db: {total_guilds}')

    @commands.command(name='blacklist', help='Blacklist a user from using the bot commands.')
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member=None):

        if not user:
            await ctx.send('Please specify a user to blacklist.')
            return

        bot_collection.update_one({}, {"$push": {"blacklisted_users": user.id}})
        await ctx.send(f'User {user.name} with id: {user.id} have been blacklisted successfully.')

    @commands.command(name='unblacklist', help='Remove a user from blacklist.')
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member=None):

        if not user:
            await ctx.send('Please specify a user to unblacklist.')
            return

        bot_collection.update_one({}, {"$pull": {"blacklisted_users": user.id}})
        await ctx.send(f'User {user.name} with id: {user.id} have been removed from blacklist successfully.')

    @commands.command(name='change_presence', help='Change presence of the bot.')
    @commands.is_owner()
    async def change_presence(self, ctx, presence_type=None, *, presence_text=None):

        types = ['playing', 'streaming', 'listening', 'watching']

        if not presence_type:
            await ctx.send('Please provide a type of presence.')
            return

        if not presence_text:
            await ctx.send('Please provide a text to be set as the bot\'s presence.')
            return
        
        if presence_type.lower() == 'playing':
            game = discord.Game(presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=game)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'streaming':
            stream = discord.Streaming(name=presence_text, url='https://www.twitch.tv/syed_ahkam')
            await ctx.bot.change_presence(status=discord.Status.online, activity=stream)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'listening':
            listening = discord.Activity(type=discord.ActivityType.listening, name=presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=listening)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'watching':
            activity = discord.Activity(type=discord.ActivityType.watching, name=presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=activity)

            await ctx.send(f'Changed presence to ``{presence_text}``')
        
        else:
            await ctx.send(f'Invalid Presence Type\nAvailable types: ``{",".join(types)}``')

    @commands.command(name='logout', help='Logout the bot from discord api.')
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('Bot is now logging out, Bye.')
        print('Bot logged out through logout command.')
        await ctx.bot.logout()

# Define setup function to make this cog loadable
def setup(bot):
    bot.add_cog(OwnerOnly(bot))
