from discord.ext import commands
from utils.logger import bot_logger
from utils.db import is_document_exists

import discord

class OwnerOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.global_blacklist_collection = bot.db.global_blacklist

    async def cog_check(self, ctx):
        """This applies a check to all the commands under this cog"""
        is_owner = await self.bot.is_owner(ctx.author)
        if not is_owner:
            raise commands.NotOwner()
            return
        return True

    @commands.command(
        name='load',
        brief='Loads a specified category.'
    )
    async def load(self, ctx, extension):
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded Successfully.')

    @commands.command(
        name='unload',
        brief='Unloads a specified category.'
    )
    async def unload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded Successfully.')

    @commands.command(
        name='reload',
        brief='Reloads a specified category.'
    )
    async def reload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} reloaded Successfully.')

    @commands.command(name='change_presence', brief='Change presence of the bot.')
    async def change_presence(self, ctx, presence_type, *, presence_text):

        types = ['playing', 'streaming', 'listening', 'watching']

        if presence_type.lower() == 'playing':
            game = discord.Game(presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=game)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'streaming':
            stream = discord.Streaming(
                name=presence_text, url='https://www.twitch.tv/syed_ahkam')
            await ctx.bot.change_presence(status=discord.Status.online, activity=stream)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'listening':
            listening = discord.Activity(
                type=discord.ActivityType.listening, name=presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=listening)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        elif presence_type.lower() == 'watching':
            activity = discord.Activity(
                type=discord.ActivityType.watching, name=presence_text)
            await ctx.bot.change_presence(status=discord.Status.online, activity=activity)

            await ctx.send(f'Changed presence to ``{presence_text}``')

        else:
            await ctx.send(f'Invalid Presence Type\nAvailable types: ``{",".join(types)}``')

    @commands.command(
        name='logout',
        brief='Logout the bot from discord api.'
    )
    async def logout(self, ctx):
        await ctx.send('Bot is now logging out, Bye.')
        bot_logger.critical('Bot logged out through logout command!')
        await ctx.bot.logout()

    @commands.command(
        name='global_blacklist',
        brief='Blacklist a user globally.'
    )
    async def global_blacklist(self, ctx, user: commands.UserConverter, *, reason=None):
        is_already_blacklisted = await is_document_exists(self.global_blacklist_collection, user.id)
        if is_already_blacklisted:
            await ctx.send('This user is already blacklisted.')
            return

        await self.global_blacklist_collection.insert_one({
            '_id': user.id,
            'reason': reason or 'No reason provided.'
        })
        await ctx.send(f'Blacklisted {user.name} globally!')

    @commands.command(
        name='global_unblacklist',
        brief='Unblacklist a user globally.'
    )
    async def global_unblacklist(self, ctx, user: commands.UserConverter):
        is_already_blacklisted = await is_document_exists(self.global_blacklist_collection, user.id)
        if not is_already_blacklisted:
            await ctx.send('This user is not blacklisted.')
            return

        await self.global_blacklist_collection.delete_one({'_id': user.id})

        await ctx.send(f'Unblacklisted {user.name} globally!')

def setup(bot):
    bot.add_cog(OwnerOnly(bot))
