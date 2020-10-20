from discord.ext import commands
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from utils.logger import bot_logger
from utils.db import get_custom_prefix
from datetime import datetime

import logging
import os
import discord
import aiohttp
import asyncio

# Uvloop
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# Setup logging
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.DEBUG)
discord_logger_handler = logging.FileHandler(
    filename='../discord.log', encoding='utf-8', mode='w')
discord_logger_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
discord_logger.addHandler(discord_logger_handler)

# Load env variables
load_dotenv()

# Intents
intents = discord.Intents.default()
intents.members = True


class Jeju(commands.Bot):
    """Subclassing bot for more control."""

    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            help_command=None,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name='+help | New and improved jeju!'),
            intents=intents
        )
        self.load_extension('jishaku')
        self.motor_client = AsyncIOMotorClient(
            os.getenv('MONGODB_URI'),
            io_loop=self.loop
        )
        self.db = self.motor_client.jeju_dev if self.is_env_dev() else self.motor_client.jeju
        self.start_time = datetime.now()
        self.loop.create_task(self.startup())

    async def get_prefix(self, message):
        """Get custom prefix depending whether they are in a guild or not."""
        default_prefix = '++' if self.is_env_dev() else '+'
        if message.guild:
            custom_prefix = await get_custom_prefix(self.db.guilds, message.guild.id)
            return commands.when_mentioned_or(custom_prefix)(self, message)
        return commands.when_mentioned_or(default_prefix)(self, message)


    @staticmethod
    def is_env_dev():
        """A simple method for checking if the bot is running in dev environment."""
        env = os.getenv('DEV', default=False)
        if env:
            return env.lower() == 'true'
        return env

    async def startup(self):
        """This function runs on startup. Used for loading cogs."""
        await self.wait_until_ready()
        ignored_cogs = ('eval')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if filename[:-3] in ignored_cogs:
                    continue
                self.load_extension(f'cogs.{filename[:-3]}')
                bot_logger.info(f'Loaded cog: {filename}')

        bot_logger.info(f'{self.user.name} connected to discord!')

        # Had to put this here because of the deprecation warning
        self.aio_session = aiohttp.ClientSession()


if __name__ == '__main__':
    # Initialize the bot
    bot = Jeju()

    if bot.is_env_dev():
        bot_logger.warning('Running in Development mode.')

    if bot.is_env_dev():
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN_DEV')
    else:
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

    if not DISCORD_TOKEN:
        bot_logger.critical('DISCORD_TOKEN environment variable not set!')

    if not os.getenv('MONGODB_URI'):
        bot_logger.critical('MONGODB_URI environment variable not set!')

    bot.run(DISCORD_TOKEN)
