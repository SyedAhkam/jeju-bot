from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import bot_logger

import logging
import os
import discord

# Setup logging
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.DEBUG)
discord_logger_handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
discord_logger_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
discord_logger.addHandler(discord_logger_handler)

load_dotenv()

class Jeju(commands.Bot):
    """Subclassing bot for more control, May help in the future."""
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            help_command=None,
            activity = discord.Activity(type=discord.ActivityType.watching, name='+help | Rewriting...')
            )

    def is_env_dev(self):
        """A simple method for checking if the bot is running in dev environment."""
        return (os.getenv('DEV').lower() == 'true')

async def get_prefix(bot, message):
    """Get custom prefix."""
    return '++' if bot.is_env_dev() else '+'

if __name__ == '__main__':
    # Initialize the bot
    bot = Jeju()

    # Load cogs from cogs directory
    ignored_cogs = ()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename[:-3] in ignored_cogs:
                continue
            bot.load_extension(f'cogs.{filename[:-3]}')
            bot_logger.info(f'Loaded cog: {filename}')


    bot.run(os.getenv('DISCORD_TOKEN_DEV' if bot.is_env_dev() else 'DISCORD_TOKEN'))
