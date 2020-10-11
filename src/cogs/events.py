from discord.ext import commands
from utils.logger import bot_logger
from utils.db import add_guild, remove_guild, delete_guild_config_values


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds_collection = bot.db.guilds
        self.config_collection = bot.db.config
        bot.after_invoke(self.command_after_invoke)

    async def command_after_invoke(self, ctx):
        """Log the invokation of a command."""
        location = ctx.guild.name if ctx.guild else 'DMs'
        bot_logger.info(
            f'Command: {ctx.command.name} invoked by the user {ctx.author.name} in {location}')

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
        await delete_guild_config_values(self.config_collection, guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
