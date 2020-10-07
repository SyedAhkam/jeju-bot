from discord.ext import commands
from utils.embeds import list_commands_under_group, error_embed, normal_embed
from utils.db import set_config_value, is_config_value_set, get_config_value, update_config_value, delete_config_value
from exceptions import AdminPermsRequiredError

class Config(commands.Cog, name='config'):
    """All of the necessary commands required to configure the bot."""

    def __init__(self, bot):
        self.bot = bot
        self.config_collection = bot.db.config

    async def cog_check(self, ctx):
        if not ctx.guild:
            return False
        if not ctx.author.guild_permissions.administrator:
            raise AdminPermsRequiredError()
        return True

    async def _enable_guild_feature(self, ctx, config_type, success_msg):
        is_config_entry_exists = await is_config_value_set(
            self.config_collection,
            ctx.guild.id,
            config_type
        )

        if is_config_entry_exists:
            is_feature_enabled = await get_config_value(
                self.config_collection,
                ctx.guild.id,
                config_type
            )

            if is_feature_enabled:
                embed = error_embed(
                    ctx,
                    error_name='Already Enabled',
                    error_msg='Sorry, This Feature is already enabled.\nIf you want to disable it then use the `disable` command.'
                )
                await ctx.send(embed=embed)
                return

        await set_config_value(
            self.config_collection,
            ctx.guild.id,
            config_type,
            True
        )

        embed = normal_embed(
            ctx,
            title='Enabled feature',
            description=success_msg
        )
        await ctx.send(embed=embed)

    async def _disable_guild_feature(self, ctx, config_type, success_msg):
        is_config_entry_exists = await is_config_value_set(
            self.config_collection,
            ctx.guild.id,
            config_type
        )

        if is_config_entry_exists:
            is_feature_enabled = await get_config_value(
                self.config_collection,
                ctx.guild.id,
                config_type
            )

            if is_feature_enabled:
                await delete_config_value(
                    self.config_collection,
                    ctx.guild.id,
                    config_type
                )

                embed = normal_embed(
                    ctx,
                    title='Disabled feature',
                    description=success_msg
                )
                await ctx.send(embed=embed)


        else:
            embed = error_embed(
                ctx,
                error_name='Already Disabled',
                error_msg='Sorry, This Feature is already disabled.\nIf you want to enable it then use the `enable` command.'
            )
            await ctx.send(embed=embed)
            return

    @commands.group(
        name='enable',
        brief='Enable certain features of the bot for your guild.',
        invoke_without_command=True
    )
    async def _enable(self, ctx):
        """**You can enable certain features of the bot using this command.**
        **Tip**: You can do just `+enable` to see all the available features.
        **Examples**: ```bash
        +enable
        +enable logging
        ```
        """
        embed = list_commands_under_group(ctx, self._enable)
        await ctx.send(embed=embed)

    @commands.group(
        name='disable',
        brief='Disable certain features of the bot for your guild.',
        invoke_without_command=True
    )
    async def _disable(self, ctx):
        """**You can disable certain features of the bot using this command.**
        **Tip**: You can do just `+disable` to see all the available features.
        **Examples**: ```bash
        +disable
        +disable logging
        ```
        """
        embed = list_commands_under_group(ctx, self._disable)
        await ctx.send(embed=embed)

    @_enable.command(
        name='logging',
        aliases=['logs'],
        brief='Enable the logging feature of the bot.'
    )
    async def enable_logging(self, ctx):
        """**You can enable the logging feature of the bot using this command.**
        **Examples**: ```bash
        +enable logging
        ```
        """
        await self._enable_guild_feature(
            ctx,
            'is_logging_enabled',
            'Successfully enabled logging in this guild/server.\nMake sure bot has the necessary permissions for the same.'
        )

    @_disable.command(
        name='logging',
        aliases=['logs'],
        brief='Disable the logging feature of the bot.'
    )
    async def disable_logging(self, ctx):
        """**You can disable the logging feature of the bot using this command.**
        **Examples**: ```bash
        +disable logging
        ```
        """
        await self._disable_guild_feature(
            ctx,
            'is_logging_enabled',
            'Successfully disabled logging in this guild/server.\nYou can use the `enable` command to enable it again.'
        )

def setup(bot):
    bot.add_cog(Config(bot))