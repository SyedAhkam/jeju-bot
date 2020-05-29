from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from jikanpy import AioJikan

import discord
import os
import datetime
import aiohttp

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds

jikan = AioJikan()


async def fetch(session, url):
    async with session.get(url) as response:
        if not response.status == 200:
            return False
        return await response.json()


class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', help='Get the bot\'s invite link.')
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def invite(self, ctx):
        # invite_url = discord.utils.oauth_url(client_id='699595477934538782', permissions='administrator', guild=None)
        invite_url = 'https://discordapp.com/api/oauth2/authorize?client_id=699595477934538782&permissions=8&scope=bot'

        embed = discord.Embed(color=0xFFFFFF, description=f'[Invite]({invite_url})', timestamp=datetime.datetime.utcnow())

        embed.set_author(name='Invite me', icon_url=ctx.bot.user.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command(name='poll', help='Build a yes or no poll.')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, type=commands.BucketType.user)
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
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def lmgtfy(self, ctx, *, query=None):
        if not query:
            await ctx.send('Please provide a query.')
            return

        joined_string = '+'.join(query.split())

        url = 'https://lmgtfy.com/?q=' + joined_string

        await ctx.send(url)

    @commands.command(name='urban', help='Get definition of a term by urban dictionary')
    @commands.cooldown(1, 5, type=commands.BucketType.user)
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

        if not example:
            example = 'None'

        embed = discord.Embed(title='Urban Dictionary', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        embed.set_footer(text='Powered by Unofficial UrbanDictionary Api')

        embed.add_field(name='Term:', value=term, inline=True)
        embed.add_field(name='URL:', value=f'[Urban]({url})', inline=True)
        embed.add_field(name='Definition:', value=definition, inline=False)   
        embed.add_field(name='Example:', value=example, inline=True)
        embed.add_field(name='Author:', value=f'[{author}]({author_url})', inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='anime', help='Get information about a specific anime.')
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def anime(self, ctx, *, anime_name=None):
        if not anime_name:
            await ctx.send('Please provide an anime name to search.')
            return

        search_response = await jikan.search(search_type='anime', query=anime_name)

        if not search_response:
            await ctx.send('Something went wrong with the api, Please try again later.')
            return

        first_result = search_response['results'][0]

        url = first_result['url']
        image_url = first_result['image_url']
        title = first_result['title']
        airing = first_result['airing']
        synopsis = first_result['synopsis']
        type = first_result['type']
        episodes = first_result['episodes']
        score = first_result['score']

        start_date = first_result['start_date']
        start_date_only = start_date.split('T')[0]
        start_datetime_object = datetime.datetime.strptime(start_date_only, '%Y-%m-%d')
        start_datetime_string = start_datetime_object.ctime()

        end_date = first_result['end_date']

        if end_date:
            end_date_only = end_date.split('T')[0]
            end_datetime_object = datetime.datetime.strptime(end_date_only, '%Y-%m-%d')
            end_datetime_string = end_datetime_object.ctime()
        else:
            end_datetime_string = 'Not ended'

        members = first_result['members']
        rated = first_result['rated']

        embed = discord.Embed(title='My Anime List', description=synopsis, color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        embed.set_footer(text='Powered by JikanAPI')

        embed.set_thumbnail(url=image_url)

        embed.add_field(name='Title:', value=f'[{title}]({url})', inline=True)
        embed.add_field(name='Airing:', value=airing, inline=True)
        embed.add_field(name='Type:', value=type, inline=True)

        embed.add_field(name='Episodes:', value=episodes, inline=True)
        embed.add_field(name='Rated:', value=rated, inline=True)
        embed.add_field(name='Score:', value=score, inline=True)

        embed.add_field(name='Members:', value=members, inline=True)
        embed.add_field(name='StartDate:', value=start_datetime_string, inline=True)
        embed.add_field(name='EndDate:', value=end_datetime_string, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='vent', help='Anonymously vent to a server\'s venting channel through DM\'s')
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def vent(self, ctx, guild_id: int=None, *, query=None):
        
        if ctx.guild:
            await ctx.send('This command can only be used in DM\'s')
            return
        
        if not guild_id:
            await ctx.send('Please provide a guild_id.')
            return
        
        if not query:
            await ctx.send('Please provide a query.')
            return
        
        guild = ctx.bot.get_guild(guild_id)

        guild_doc = guilds_collection.find_one(filter={"guild_id": guild.id})

        if not 'venting_channel' in guild_doc:
            await ctx.send('Please ask the server admins to setup a venting channel using the command ``set_venting_channel``.')
            return
        
        if not guild_doc['venting_channel']:
            await ctx.send('Please ask the server admins to setup a venting channel using the command ``set_venting_channel``.')
            return
        
        venting_channel_id = guild_doc['venting_channel']

        venting_channel = guild.get_channel(venting_channel_id)

        print(f'{ctx.author.name} with id: {ctx.author.id} used the venting command.')

        await venting_channel.send("**Vent:**" + "\n" + query)
        await ctx.send('Successfully sent your venting message.')

    @commands.command(name='emoji', help='Get your favorite emoji as a picture.')
    @commands.cooldown(1,3, type=commands.BucketType.user)
    async def emoji(self, ctx, emoji: commands.EmojiConverter= None):
        if not emoji:
            await ctx.send('Please provide a emoji.')
            return
        
        embed = discord.Embed(color=0xFFFFFF)

        embed.set_image(url=emoji.url)

        await ctx.send(embed=embed)

    @commands.command(name='time_in', help='Find the current time in different timezones.')
    @commands.cooldown(1,5, type=commands.BucketType.user)
    async def time_in(self, ctx, *, timezone=None):
        if not timezone:
            await ctx.send('Please provide a timezone.\nAvailable timezones: http://worldtimeapi.org/timezones')
            return

        base_url = 'https://worldtimeapi.org/api/timezone/'
        url_to_request = base_url + timezone

        async with aiohttp.ClientSession() as session:
            response = await fetch(session, url_to_request)

        if not response:
            await ctx.send('Invalid Timezone or something\'s wrong with the API.\nAvailable timezones: http://worldtimeapi.org/timezones')
            return

        if type(response) is list:
            await ctx.send('Invalid Timezone or something\'s wrong with the API.\nAvailable timezones: http://worldtimeapi.org/timezones')
            return

        datetime_str = response['datetime']

        abbreviation = response['abbreviation']
        day_of_week = response['day_of_week']
        day_of_year = response['day_of_year']
        is_dst = response['dst']
        dst_from = response['dst_from']
        dst_offset = response['dst_offset']
        dst_until = response['dst_until']
        raw_offset = response['raw_offset']
        utc_datetime = response['utc_datetime']
        utc_offset = response['utc_offset']
        week_number = response['week_number']


        format_string = "%Y-%m-%dT%H:%M:%S.%f%z"

        if datetime_str:
            datetime_obj = datetime.datetime.strptime(datetime_str, format_string)
            date = f'{datetime_obj.month}/{datetime_obj.day}/{datetime_obj.year}\n[Month/Day/Year]'
            time = f'{datetime_obj.hour}:{datetime_obj.minute}:{datetime_obj.second}\n[Hour:Minute:Seconds]'
        else:
            date = None
            time = None

        if utc_datetime:
            datetime_utc_obj = datetime.datetime.strptime(utc_datetime, format_string)
            date_utc = f'{datetime_utc_obj.month}/{datetime_utc_obj.day}/{datetime_utc_obj.year}\n[Month/Day/Year]'
            time_utc = f'{datetime_utc_obj.hour}:{datetime_utc_obj.minute}:{datetime_utc_obj.second}\n[Hour:Minute:Seconds]'
        else:
            date_utc = None
            time_utc = None

        if dst_from:
            datetime_dst_from_obj = datetime.datetime.strptime(dst_from.split('+')[0], "%Y-%m-%dT%H:%M:%S")
            date_dst_from = f'{datetime_dst_from_obj.month}/{datetime_dst_from_obj.day}/{datetime_dst_from_obj.year}\n[Month/Day/Year]'
            time_dst_from = f'{datetime_dst_from_obj.hour}:{datetime_dst_from_obj.minute}:{datetime_dst_from_obj.second}\n[Hour:Minute:Seconds]'
        else:
            date_dst_from = None
            time_dst_from = None

        if dst_until:
            datetime_dst_until_obj = datetime.datetime.strptime(dst_until.split('+')[0], "%Y-%m-%dT%H:%M:%S")
            date_dst_until = f'{datetime_dst_until_obj.month}/{datetime_dst_until_obj.day}/{datetime_dst_until_obj.year}\n[Month/Day/Year]'
            time_dst_until = f'{datetime_dst_until_obj.hour}:{datetime_dst_until_obj.minute}:{datetime_dst_until_obj.second}\n[Hour:Minute:Seconds]'
        else:
            date_dst_until = None
            time_dst_until = None

        embed = discord.Embed(title=f'Time in {timezone}', color=0xFFFFFF, timestamp=datetime.datetime.utcnow())

        embed.set_footer(text='Powered by WorldTimeAPI')

        embed.add_field(name='DST:', value=is_dst, inline=True)
        embed.add_field(name='Date:', value=date, inline=True)
        embed.add_field(name='Time:', value=time, inline=True)

        embed.add_field(name='Day Of Week:', value=day_of_week, inline=True)
        embed.add_field(name='Day Of Year: ', value=day_of_year, inline=True)
        embed.add_field(name='Week Number:', value=week_number, inline=True)

        if date_dst_from and time_dst_from:
            embed.add_field(name='DST From:', value=date_dst_from + '\n' + time_dst_from, inline=True)
        else:
            embed.add_field(name='DST From:', value=None, inline=True)

        embed.add_field(name='DST Offset:', value=dst_offset, inline=True)

        if date_dst_until and time_dst_until:
            embed.add_field(name='DST Until:', value=date_dst_until + '\n' + time_dst_until, inline=True)
        else:
            embed.add_field(name='DST Until:', value=None, inline=True)

        embed.add_field(name='Raw Offset:', value=raw_offset, inline=True)
        embed.add_field(name='UTC DateTime:', value=date_utc + '\n' + time_utc, inline=True)
        embed.add_field(name='UTC Offset:', value=utc_offset, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
