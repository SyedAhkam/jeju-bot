from discord.ext import commands
from utils.logger import bot_logger
from utils.db import add_guild, remove_guild, delete_guild_config_values, get_custom_prefix
from utils.embeds import normal_embed_using_message


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

    @commands.Cog.listener()
    async def on_message(self, message):
        """on_message event used to detect the bot mention and reply with the prefixes."""
        if message.author == self.bot.user:
            return

        if message.guild.me in message.mentions:
            default_prefix = '++' if self.bot.is_env_dev() else '+'
            if not message.guild:
                prefixes = [default_prefix, message.guild.me.mention]
            else:
                custom_prefix = await get_custom_prefix(
                    self.guilds_collection,
                    message.guild.id
                )
                prefixes = [custom_prefix, message.guild.me.mention]

            prefixes_string = ', '.join(prefixes)
            embed = normal_embed_using_message(
                message,
                self.bot,
                title='Prefixes',
                description=f'Hi, Did you forget my prefix? No worries.\nMy prefixes are {prefixes_string}.'
            )

            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
