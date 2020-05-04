from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import os
import datetime
import aiohttp

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds

async def fetch(session, url):
    async with session.get(url) as response:
        if not response.status == 200:
            return False
        return await response.json()

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', help='Get the bot\'s invite link.')
    async def invite(self, ctx):
        # invite_url = discord.utils.oauth_url(client_id='699595477934538782', permissions='administrator', guild=None)
        invite_url = 'https://discordapp.com/api/oauth2/authorize?client_id=699595477934538782&permissions=8&scope=bot'

        embed = discord.Embed(color=0xFFFFFF, description=f'[Invite]({invite_url})', timestamp=datetime.datetime.utcnow())

        embed.set_author(name='Invite me', icon_url=ctx.bot.user.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command(name='poll', help='Build a yes or no poll.')
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, question=None):
        if not question:
            await ctx.send('Please provide a question.')
            return
        
        embed = discord.Embed(title='Poll', color=0xFFFFFF, description=question, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        embed.add_field(name='React', value='✅Yes ❌No')

        await ctx.message.delete()
        msg = await ctx.send(embed=embed)

        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

    @commands.command(name='lmgtfy', help='Help your friends who doesn\'t know how to use google.')
    async def lmgtfy(self, ctx, *, query=None):
        if not query:
            await ctx.send('Please provide a query.')
            return

        joined_string = '+'.join(query.split())

        url = 'https://lmgtfy.com/?q=' + joined_string

        await ctx.send(url)

    @commands.command(name='urban', help='Get definition of a term by urban dictionary')
    async def urban(self, ctx, *, query=None):
        if not query:
            await ctx.send('Please provide a query.')
            return

        async with aiohttp.ClientSession() as session:
            response = await fetch(session, f'http://urbanscraper.herokuapp.com/define/{query}')
        if not response:
            await ctx.send('Couldn\'t find definition for the term provided by you.')
            return

        term = response['term']
        url = response['url']
        definition = response['definition']
        example = response['example']
        author = response['author']
        author_url = response['author_url']

        embed = discord.Embed(title='Urban Dictionary', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        embed.set_footer(text='Powered by Unofficial UrbanDictionary Api')

        embed.add_field(name='Term:', value=term, inline=True)
        embed.add_field(name='URL:', value=f'[Urban]({url})', inline=True)
        embed.add_field(name='Definition:', value=definition, inline=False)
        if not example:
            embed.add_field(name='Example:', value='None', inline=True)
        else:    
            embed.add_field(name='Example:', value=example, inline=True)
        embed.add_field(name='Author:', value=f'[{author}]({author_url})', inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
