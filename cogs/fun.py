import discord
from discord.ext import commands

import random
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

from pymongo import MongoClient
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', help='Says back hello to the user.')
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}')

    @commands.command(name='roll', help='Simulates a dice roll.')
    async def roll(self, ctx, number_of_dice: int=None, number_of_sides: int=6):

        if not number_of_dice:
            await ctx.send('Please provide number of dices.')
            return

        if number_of_dice > 10:
            await ctx.send('Please keep the number of dices less than 10.')
            return

        if number_of_sides > 100:
            await ctx.send('Please keep the number of sides less than 100.')
            return

        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for dice in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(name='8ball', aliases=['ball'], help='Ask any yes or no question to 8ball.')
    async def _8ball(self, ctx, *, question=None):

        if not question:
            await ctx.send('You need to ask me a question too.')
            return

        responses_collection = db.responses
        response = responses_collection.find_one()['8ball']

        choosen_response = random.choice(response)

        embed = discord.Embed(title=f'You asked \'{question}\'', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
        ), footer=f'Asked by {ctx.author.name}')

        embed.add_field(name='Magic 8ball thinks:', value=choosen_response, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
