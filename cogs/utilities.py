import discord
from discord.ext import commands

class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', help='Get the bot\'s invite link.')
    async def invite(self, ctx):
        #invite_url = discord.utils.oauth_url(client_id='699595477934538782', permissions='administrator', guild=None)
        invite_url = 'https://discordapp.com/api/oauth2/authorize?client_id=699595477934538782&permissions=8&scope=bot'
        await ctx.send(f'Invite me using this link:\n{invite_url}')

def setup(bot):
    bot.add_cog(Utilities(bot))