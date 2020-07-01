# Imports
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urlextract import URLExtract

import discord
import random
import datetime
import os
import aiohttp

# Load env variables
load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

# Initialize the mongo_client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju

# Initialize the urlextract thing
extractor = URLExtract()

# Define fetch function
async def fetch(session, url):
    async with session.get(url) as response:
        if not response.status == 200:
            return False
        return await response.json()


# Main Cog Class
class Fun(commands.Cog):

    # Initialize the class
    def __init__(self, bot):
        self.bot = bot

    #Commands
    @commands.command(name='hello', help='Says back hello to the user.', aliases=['hi', 'hey'])
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}.')

    @commands.command(name='roll', help='Simulates a dice roll.')
    @commands.cooldown(1, 5, type=commands.BucketType.user)
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
    @commands.cooldown(1, 3, type=commands.BucketType.user)
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
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def meme(self, ctx):

        async with aiohttp.ClientSession() as session:
            response = await fetch(session, 'https://meme-api.herokuapp.com/gimme')

        if not response:
            await ctx.send('Something went wrong with the API, Please try again later.')
            return

        post_link = response['postLink']
        subreddit = response['subreddit']
        title = response['title']
        image_url = response['url']

        embed = discord.Embed(title='A random meme for you', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text='Powered by MemeAPI')
        embed.set_image(url=image_url)

        embed.add_field(name='Title:', value=title)
        embed.add_field(name='PostLink:', value=f'[Post]({post_link})')
        embed.add_field(name='SubReddit', value=subreddit)

        await ctx.send(embed=embed)

    @commands.command(name='vibe_check', help='Get your vibe checked')
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def vibe_check(self, ctx, *, name=None):
        url = 'https://en.shindanmaker.com/937709'

        if not name:
            data = {'u': ctx.author.name}
        else:
            data = {'u': name}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if not response.status == 200:
                    return False
                response = await response.text()


        if not response:
            await ctx.send('Something got wrong while getting the response, Try again later.')
            return

        doc = BeautifulSoup(response, 'html.parser')

        text = doc.textarea.contents[0]

        passed = 'Undefined'

        if 'Vibe check passed' in text:
            passed = True
        if 'Vibe check failed' in text:
            passed = False

        result_url = extractor.find_urls(text)[0]

        if passed:
            await ctx.send(f'Congratulations you passed the vibe check!\nURL: {result_url}')
            return
        await ctx.send(f'Sorry you failed the vibe check :(\nURL: {result_url}')


# Define setup function to make this cog loadable
def setup(bot):
    bot.add_cog(Fun(bot))
