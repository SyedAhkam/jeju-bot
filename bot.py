import logging
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import os
import datetime

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju

guilds_collection = db.guilds
bot_collection = db.bot


def get_prefix(bot, message):
    if message.guild:
        guild = guilds_collection.find_one(filter={"guild_id": message.guild.id})
        return commands.when_mentioned_or(guild['guild_prefix'])(bot, message)

    return commands.when_mentioned_or('+')(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.start_time = datetime.datetime.now()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord!')

    activity = discord.Activity(type=discord.ActivityType.watching, name="+help | In Development")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Status changed')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    blacklisted_users = bot_collection.find_one()['blacklisted_users']
    if message.author.id in blacklisted_users:

        if message.guild:
            guild = guilds_collection.find_one(filter={"guild_id": message.guild.id})
            prefix = guild['guild_prefix']
        else:
            prefix = '+'

        if message.content.startswith(prefix):
            await message.channel.send('Sorry, you have been blacklisted from using this bot.\nAsk the bot owner to remove you from blacklist.')
            return

    if bot.user.mentioned_in(message):
        if message.guild:
            guild = guilds_collection.find_one(filter={"guild_id": message.guild.id})
            prefixes = [str(guild['guild_prefix']), '@mention']
        else:
            prefixes = ['+', '@mention']

        prefixes = ', '.join(prefixes)
        await message.channel.send(f'My prefixes are ``{prefixes}``')

    await bot.process_commands(message)


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
        "guild_features": guild.features,
        "mod_role": None,
        "modlog_channel": None,
        "venting_channel": None
    }
    guilds_collection.insert_one(post)


@bot.event
async def on_guild_remove(guild):
    guilds_collection.delete_one(filter={"guild_id": guild.id})


@bot.event
async def on_command_error(ctx, error):

    ignored = (commands.errors.CommandNotFound)

    error = getattr(error, "original", error)

    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.errors.DisabledCommand):
        return await ctx.send(f'This command has been disabled by the owner, Ask them to enable it.')

    elif isinstance(error, commands.errors.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} command can not be used in Private Messages.')
            except:
                pass
    
    elif isinstance(error, commands.errors.CheckFailure):
        if isinstance(error, commands.errors.NotOwner):
            return await ctx.send('This command is only accessible by the owner of the bot.')
        elif isinstance(error, commands.errors.MissingPermissions):
            return await ctx.send(f'Looks like you don\'t have permission to access this command.\nPermissions required: ``{error.missing_perms}``')
        elif isinstance(error, commands.errors.BotMissingPermissions):
            return await ctx.send(f'Bot need these permissions to run that command, ``{error.missing_perms}``')
        elif isinstance(error, commands.errors.MissingRole):
            return await ctx.send(f'You need this role to access this command: ``{error.missing_role}``')
    
    elif isinstance(error, commands.errors.BadArgument):
        return await ctx.send('Invalid arguments given, please check the help command.')
    
    elif isinstance(error, commands.errors.CommandOnCooldown):
        return await ctx.send(f'This command is on cooldown.\n Please wait ``{round(error.retry_after)}`` more seconds.')

    elif isinstance(error, commands.errors.ExtensionError):
        if isinstance(error,commands.errors.ExtensionNotFound):
            return await ctx.send(f'Extension with name ``{error.name}`` not found.')
        elif isinstance(error,commands.errors.ExtensionAlreadyLoaded):
            return await ctx.send(f'Extension with name ``{error.name}`` already loaded.')
        elif isinstance(error,commands.errors.ExtensionNotLoaded):
            return await ctx.send(f'Extension with name ``{error.name}`` not loaded.')
        elif isinstance(error, commands.errors.ExtensionFailed):
            return await ctx.send(f'Extension with name ``{error.name}`` failed to load.')
    
    else:
        await ctx.send('An unexpected error occured.')
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

bot.run(TOKEN)
