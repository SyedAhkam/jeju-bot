import discord

from discord.ext import commands
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGODB_URI')

from pymongo import MongoClient
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds

def get_prefix(bot, message):
    if message.guild:
        guild = guilds_collection.find_one(filter={"guild_id": message.guild.id})
        return guild['guild_prefix']

    else:
        return "+"

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord!')
    #game = discord.Game(name="+help | In Development")
    activity = discord.Activity(type=discord.ActivityType.watching, name="+help | In Development")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Status changed')

@bot.event
async def on_guild_join(guild):

        post = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "guild_prefix": "+",
            "guild_region": guild.region,
            "guild_icon": guild.icon,
            "guild_owner_id": guild.owner_id,
            "members": len(guild.members),
            "guild_description": guild.description,
            "guild_verification": guild.verification_level,
            "guild_features": guild.features
        }
        guilds_collection.insert_one(post)

@bot.event
async def on_guild_remove(guild):
    guilds_collection.delete_one(filter={"guild_id": guild.id})

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Looks like you don\'t have permission to access this command.')
    else:
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

bot.run(TOKEN)