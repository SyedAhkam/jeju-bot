from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

import discord
import datetime
import ago
import os

load_dotenv()
MONGO_URI = os.getenv('MONGODB_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.jeju
guilds_collection = db.guilds


class Info(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping = round(ctx.bot.latency * 1000)
        await ctx.send(f'Pong!\n{ping}ms')

    @commands.command()
    async def user(self, ctx, user: commands.MemberConverter = None):

        if not user:
            user_name = ctx.author.name
            user_id = ctx.author.id
            user_discriminator = ctx.author.discriminator
            created_at = ago.human(ctx.author.created_at, 4)
            display_name = ctx.author.display_name
            joined_at = ago.human(ctx.author.joined_at, 4)
            status = ctx.author.status
            avatar_url = ctx.author.avatar_url
            roles = ctx.author.roles
            activity = ctx.author.activity

            roles_string = ''

            for role in roles:
                roles_string += role.name + ', '

            embed_author = discord.Embed(title='Your info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
            ), footer=f'Requested by {ctx.author.name}')

            embed_author.set_author(name=user_name, url=discord.Embed.Empty, icon_url=avatar_url)

            embed_author.set_thumbnail(url=avatar_url)

            embed_author.add_field(name='UserName:', value=user_name, inline=True)
            embed_author.add_field(name='UserID:', value=user_id, inline=True)
            embed_author.add_field(name='UserTag:', value=user_name + '#' + user_discriminator, inline=True)

            if not user_name == display_name:
                embed_author.add_field(name='Nickname:', value=display_name, inline=False)
            else:
                embed_author.add_field(name='Nickname:', value='None', inline=False)

            embed_author.add_field(name='Created:', value=created_at, inline=True)
            embed_author.add_field(name='Joined:', value=joined_at, inline=True)
            embed_author.add_field(name='Status:', value=status, inline=False)

            if not activity:
                embed_author.add_field(name='Activity:', value='No activity', inline=True)
            else:
                embed_author.add_field(name='Activity:', value=activity.name, inline=True)

            embed_author.add_field(name='Roles:', value=f'```{roles_string}```', inline=False)

            await ctx.send(embed=embed_author)
            return

        embed_user = discord.Embed(title=f'{user.name}\'s info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
        ), footer=f'Requested by {ctx.author.name}')

        user_name = user.name
        user_id = user.id
        user_discriminator = user.discriminator
        is_bot = user.bot
        created_at = ago.human(user.created_at, 4)
        display_name = user.display_name
        joined_at = ago.human(user.joined_at, 4)
        status = user.status
        avatar_url = user.avatar_url
        roles = user.roles
        activity = user.activity

        roles_string = ''

        for role in roles:
            roles_string += role.name + ', '

        embed_user.set_author(name=user_name, url=discord.Embed.Empty, icon_url=avatar_url)

        embed_user.set_thumbnail(url=avatar_url)

        embed_user.add_field(name='UserName:', value=user_name, inline=True)
        embed_user.add_field(name='UserID:', value=user_id, inline=True)
        embed_user.add_field(name='UserTag:', value=user_name + '#' + user_discriminator, inline=True)

        if not user_name == display_name:
            embed_user.add_field(name='Nickname:', value=display_name, inline=False)
        else:
            embed_user.add_field(name='Nickname:', value='None', inline=False)

        embed_user.add_field(name='Bot:', value=is_bot, inline=True)
        embed_user.add_field(name='Created:', value=created_at, inline=False)
        embed_user.add_field(name='Joined:', value=joined_at, inline=True)

        embed_user.add_field(name='Status:', value=status, inline=True)

        if not activity:
            embed_user.add_field(name='Activity:', value='No activity', inline=True)
        else:
            embed_user.add_field(name='Activity:', value=activity.name, inline=True)

        embed_user.add_field(name='Roles:', value=f'```{roles_string}```', inline=False)

        await ctx.send(embed=embed_user)

    @commands.command(name='server', help='Get information about the server or guild.')
    async def server(self, ctx):

        guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})

        guild_id = ctx.guild.id
        guild_name = ctx.guild.name
        guild_prefix = guild["guild_prefix"]
        guild_region = ctx.guild.region
        guild_icon_url = ctx.guild.icon_url
        guild_owner = ctx.guild.owner
        guild_members = len(ctx.guild.members)
        guild_verification = ctx.guild.verification_level
        guild_features = ctx.guild.features
        guild_emojis = ctx.guild.emojis
        guild_afk_channel = ctx.guild.afk_channel
        guild_default_notifications = ctx.guild.default_notifications
        guild_boost_tier = ctx.guild.premium_tier
        guild_boosters = ctx.guild.premium_subscription_count
        guild_channels = len(ctx.guild.channels)
        guild_text_channels = len(ctx.guild.text_channels)
        guild_voice_channels = len(ctx.guild.voice_channels)
        guild_categories = len(ctx.guild.categories)
        guild_emoji_limit = ctx.guild.emoji_limit
        guild_roles = len(ctx.guild.roles)
        guild_created_at = ago.human(ctx.guild.created_at, 4)

        emojis_string = ''

        for emoji in guild_emojis:
            emojis_string += f'<:{emoji.name}:{emoji.id}>, '

        if len(emojis_string) > 1024:
            emojis_string = 'Too many emojis to show here.'

        embed = discord.Embed(title='Server info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
        ), footer=f'Requested by {ctx.author.name}')

        embed.set_thumbnail(url=guild_icon_url)

        embed.add_field(name='Name:', value=guild_name, inline=True)
        embed.add_field(name='Id:', value=guild_id, inline=True)
        embed.add_field(name='Prefix:', value=guild_prefix, inline=True)

        embed.add_field(name='Region:', value=guild_region, inline=True)
        embed.add_field(name='Owner:', value=guild_owner.mention, inline=True)
        embed.add_field(name='Members:', value=guild_members, inline=True)

        embed.add_field(name='Verification level:', value=guild_verification, inline=True)
        embed.add_field(name='AFK Channel:', value=guild_afk_channel, inline=True)
        embed.add_field(name='Default Notifications:', value=guild_default_notifications, inline=True)

        embed.add_field(name='Boost Tier:', value=guild_boost_tier, inline=True)
        embed.add_field(name='Boosters:', value=guild_boosters, inline=True)
        embed.add_field(name='Features:', value=guild_features, inline=True)

        embed.add_field(name='Text Channels:', value=guild_text_channels, inline=True)
        embed.add_field(name='Voice Channels:', value=guild_voice_channels, inline=True)
        embed.add_field(name='Total Channels:', value=guild_channels, inline=True)

        embed.add_field(name='Categories:', value=guild_categories, inline=True)
        embed.add_field(name='Roles:', value=guild_roles, inline=True)
        embed.add_field(name='Created:', value=guild_created_at, inline=True)

        embed.add_field(name='Emoji limit:', value=guild_emoji_limit, inline=True)

        embed.add_field(name='Emojis:', value=emojis_string, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='bot', help='Get some info about the bot.')
    async def bot(self, ctx):

        if ctx.guild:
            guild = guilds_collection.find_one(filter={"guild_id": ctx.guild.id})
            prefixes = [str(guild['guild_prefix']), '@mention']
        else:
            prefixes = ['+', '@mention']

        prefixes = ', '.join(prefixes)

        ping = round(ctx.bot.latency * 1000)

        embed = discord.Embed(title='Bot info', color=0xFFFFFF, timestamp=datetime.datetime.utcnow(
        ), footer=f'Requested by {ctx.author.name}')

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)

        embed.add_field(name='Name:', value=ctx.bot.user.name, inline=True)
        embed.add_field(name='Developer:', value='SyedAhkam#8605', inline=True)
        embed.add_field(name='Library:', value=f'discord.py {discord.__version__}', inline=True)

        embed.add_field(name='Guilds:', value=len(ctx.bot.guilds), inline=True)
        embed.add_field(name='Users:', value=len(ctx.bot.users), inline=True)
        embed.add_field(name='Prefixes:', value=prefixes, inline=True)

        embed.add_field(name='Ping:', value=f'{ping}ms', inline=True)
        embed.add_field(name='Source:', value='[link](https://github.com/SyedAhkam/jeju-bot/)')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
