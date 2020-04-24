from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import os

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

    @commands.command(name='change_prefix', help='Change the bot\'s prefix.')
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix=None):
        if not prefix:
            await ctx.send('Please specify a prefix.')
            return

        guilds_collection.find_one_and_update({"guild_id": ctx.guild.id}, {'$set': {"guild_prefix": prefix}})

        await ctx.send(f'Prefix set to ``{prefix}``')


def setup(bot):
    bot.add_cog(Utilities(bot))
