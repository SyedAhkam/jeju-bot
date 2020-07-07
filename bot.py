# Imports
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import logging
import discord
import os
import datetime

# SetUp Logging
logging.basicConfig(level=logging.INFO)

# Load the env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGODB_URI')

# Initialize MongoClient
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju

# Get some collections
guilds_collection = db.guilds
bot_collection = db.bot


# Get custom prefix
def get_prefix(bot, message):

    # If it is a guild then find a custom prefix
    if message.guild:
        guild = guilds_collection.find_one(
            filter={"guild_id": message.guild.id})
        return commands.when_mentioned_or(guild['guild_prefix'])(bot, message)

    # Else default to +
    return commands.when_mentioned_or('+')(bot, message)


# Initialize the bot
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
# Store the start time to calculate uptime later
bot.start_time = datetime.datetime.now()

# On_ready event


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord!')

    # Change the presence
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="+help | In Development")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Status changed')


# on_message event
@bot.event
async def on_message(message):
    # If the message is sent by the bot itself, return
    if message.author == bot.user:
        return

    # Check if the user is blacklisted
    blacklisted_users = bot_collection.find_one()['blacklisted_users']
    if message.author.id in blacklisted_users:

        # Get the prefix
        if message.guild:
            guild = guilds_collection.find_one(
                filter={"guild_id": message.guild.id})
            prefix = guild['guild_prefix']
        else:
            prefix = '+'

        # Check if the blacklisted user is trying to interact with the bot
        if message.content.startswith(prefix):
            await message.channel.send('Sorry, you have been blacklisted from using this bot.\nAsk the bot owner to remove you from blacklist.')
            return

    # If mentioned in in a message, then tell the user available prefixes
    if bot.user.mentioned_in(message):
        if message.guild:
            guild = guilds_collection.find_one(
                filter={"guild_id": message.guild.id})
            prefixes = [str(guild['guild_prefix']), '@mention']
        else:
            prefixes = ['+', '@mention']

        prefixes = ', '.join(prefixes)
        await message.channel.send(f'My prefixes are ``{prefixes}``')

    # IMPORTANT: Process the commands after everything is alright
    await bot.process_commands(message)

# on_member_join event


@bot.event
async def on_member_join(member):

    guild_doc = guilds_collection.find_one(
        filter={"guild_id": member.guild.id})

    # Check if a join message is set in the guild
    if 'join_channel' not in guild_doc:
        return

    if not guild_doc['join_channel']:
        return

    if 'join_message' not in guild_doc:
        return

    if not guild_doc['join_message']:
        return

    # If yes then format it if needed
    join_channel = member.guild.get_channel(guild_doc['join_channel'])

    formatted_message = guild_doc['join_message']

    if '{user}' in formatted_message:
        formatted_message = formatted_message.replace('{user}', member.name)

    if '{user_mention}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_mention}', member.mention)

    if '{user_id}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_id}', str(member.id))

    if '{user_tag}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_tag}', f'{member.name}#{member.discriminator}')

    if '{server}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{server}', member.guild.name)

    if '{server_members}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{server_members}', len(member.guild.members))

    # Then finally send it to the join_channel
    await join_channel.send(formatted_message)

# on_member_remove event


@bot.event
async def on_member_remove(member):

    guild_doc = guilds_collection.find_one(
        filter={"guild_id": member.guild.id})

    # Check if a leave message is set in the guild
    if 'leave_channel' not in guild_doc:
        return

    if not guild_doc['leave_channel']:
        return

    if not 'leave_message' in guild_doc:
        return

    if not guild_doc['leave_message']:
        return

    # If yes then format it if needed
    leave_channel = member.guild.get_channel(guild_doc['leave_channel'])

    formatted_message = guild_doc['leave_message']

    if '{user}' in formatted_message:
        formatted_message = formatted_message.replace('{user}', member.name)

    if '{user_mention}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_mention}', member.mention)

    if '{user_id}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_id}', str(member.id))

    if '{user_tag}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{user_tag}', f'{member.name}#{member.discriminator}')

    if '{server}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{server}', member.guild.name)

    if '{server_members}' in formatted_message:
        formatted_message = formatted_message.replace(
            '{server_members}', len(member.guild.members))

    # Then finally send it to the leave_channel
    await leave_channel.send(formatted_message)

# on_guild_join event, Just to get the guild info in db


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
        "venting_channel": None,
        "join_channel": None,
        "leave_channel": None,
        "join_message": None,
        "join_message_set": False,
        "leave_message": None,
        "leave_message_set": False,
        "verified_role": None
    }
    guilds_collection.insert_one(post)


# on_guild_remove event, Delete the document which contains info about the guild
@bot.event
async def on_guild_remove(guild):
    guilds_collection.delete_one(filter={"guild_id": guild.id})


# On_command_error event, used as a error handler
@bot.event
async def on_command_error(ctx, error):

    # Ignore some errors
    ignored = (commands.errors.CommandNotFound)

    error = getattr(error, "original", error)

    if isinstance(error, ignored):
        return

    # Catching other errors
    elif isinstance(error, commands.errors.DisabledCommand):
        return await ctx.send('This command has been disabled by the owner, Ask them to enable it.')

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
        if isinstance(error, commands.errors.ExtensionNotFound):
            return await ctx.send(f'Extension with name ``{error.name}`` not found.')
        elif isinstance(error, commands.errors.ExtensionAlreadyLoaded):
            return await ctx.send(f'Extension with name ``{error.name}`` already loaded.')
        elif isinstance(error, commands.errors.ExtensionNotLoaded):
            return await ctx.send(f'Extension with name ``{error.name}`` not loaded.')
        elif isinstance(error, commands.errors.ExtensionFailed):
            return await ctx.send(f'Extension with name ``{error.name}`` failed to load.')

    # If the error is not handled, then raise error
    else:
        await ctx.send('An unexpected error occured.')
        raise error

# Load the cogs in cogs directory
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

# Finally run the bot
bot.run(TOKEN)
