import discord

from discord.ext import commands
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord!')
    #game = discord.Game(name="+help | In Development")
    activity = discord.Activity(type=discord.ActivityType.watching, name="+help | In Development")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Status changed')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
    print('An error occured')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Looks like you don\'t have permission to access this command.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

bot.run(TOKEN)