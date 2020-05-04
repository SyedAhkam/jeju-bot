from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import random
import datetime
import os
import aiohttp

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


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

        embed = discord.Embed(title=f'You asked \'{question}\'', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        embed.set_footer(text=f'Asked by {ctx.author.name}')

        embed.add_field(name='Magic 8ball thinks:', value=choosen_response, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='meme', help='Get a random meme from reddit.')
    async def meme(self, ctx):

        async with aiohttp.ClientSession() as session:
            json = await fetch(session, 'https://meme-api.herokuapp.com/gimme')
            
        post_link = json['postLink']
        subreddit = json['subreddit']
        title = json['title']
        image_url = json['url']

        embed = discord.Embed(title='A random meme for you', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text='Powered by MemeAPI')
        embed.set_image(url=image_url)

        embed.add_field(name='Title:', value=title)
        embed.add_field(name='PostLink:', value=f'[Post]({post_link})')
        embed.add_field(name='SubReddit', value=subreddit)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
