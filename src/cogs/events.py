from discord.ext import commands
from utils.logger import bot_logger
from utils.db import add_guild, remove_guild

# TODO: on_member_join and on_member_remove maybe on_message too

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds_collection = bot.db.guilds
        bot.after_invoke(self.command_after_invoke)

    async def command_after_invoke(self, ctx):
        """Log the invokation of a command."""
        bot_logger.info(f'Command: {ctx.command.name} invoked by the user {ctx.author.name} in {ctx.guild.name}')

    @commands.Cog.listener()
    async def on_ready(self):
        """On ready event, very helpful."""
        bot_logger.info(f'{self.bot.user.name} connected to discord!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Notify the guild owner on joining a new server and saving guild in db."""
        app_info = await self.bot.application_info()
        await app_info.owner.send(f'I got added to a new server: {guild.name} with {len(guild.members)} members!!')

        await add_guild(self.guilds_collection, guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Notify the guild owner on leaving a server and removing guild from db."""
        app_info = await self.bot.application_info()
        await app_info.owner.send(f'I got removed from this server: {guild.name} with {len(guild.members)} members :(')

        await remove_guild(self.guilds_collection, guild.id)

def setup(bot):
    bot.add_cog(Events(bot))
