from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import os
import datetime

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds


class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', help='Get the bot\'s invite link.')
    async def invite(self, ctx):
        # invite_url = discord.utils.oauth_url(client_id='699595477934538782', permissions='administrator', guild=None)
        invite_url = 'https://discordapp.com/api/oauth2/authorize?client_id=699595477934538782&permissions=8&scope=bot'
        await ctx.send(f'Invite me using this link:\n{invite_url}')
    
    @commands.command(name='poll', help='Build a yes or no poll.')
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, question=None):
        if not question:
            await ctx.send('Please provide a question.')
            return
        
        embed = discord.Embed(title='Poll', color=0xFFFFFF, description=question, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f'Poll by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        embed.add_field(name='React', value='✅Yes ❌No')

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('✅')
        await msg.add_reaction('❌')


def setup(bot):
    bot.add_cog(Utilities(bot))
