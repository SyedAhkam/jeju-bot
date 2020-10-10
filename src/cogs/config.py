from discord.ext import commands
from utils.embeds import list_commands_under_group, error_embed, normal_embed
from utils.db import set_config_value, is_config_value_set, get_config_value, update_config_value, delete_config_value, set_custom_prefix
from exceptions import AdminPermsRequiredError


class Config(commands.Cog, name='config'):
    """All of the necessary commands required to configure the bot."""

    def __init__(self, bot):
        self.bot = bot
        self.config_collection = bot.db.config
        self.guilds_collection = bot.db.guilds
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            1,
            7,
            commands.BucketType.member
        )

    async def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage()
        if not ctx.author.guild_permissions.administrator:
            raise AdminPermsRequiredError()
        bucket = self.cd_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(self.cd_mapping, retry_after)
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

    async def _set_config_value(self, ctx, config_type, config_value, success_msg):
        is_config_entry_exists = await is_config_value_set(
            self.config_collection,
            ctx.guild.id,
            config_type
        )

        if is_config_entry_exists:
            await update_config_value(
                self.config_collection,
                ctx.guild.id,
                config_type,
                config_value
            )

            embed = normal_embed(
                ctx,
                title='Set config value',
                description=success_msg
            )
            await ctx.send(embed=embed)

        else:
            await set_config_value(
                self.config_collection,
                ctx.guild.id,
                config_type,
                config_value
            )

            embed = normal_embed(
                ctx,
                title='Set config value',
                description=success_msg
            )
            await ctx.send(embed=embed)

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

    @commands.group(
        name='set',
        brief='Set certain values required by the bot to customize features of the bot.',
        invoke_without_command=True
    )
    async def _set(self, ctx):
        """**You can set certain values of the bot using this command.**
        **Tip**: You can do just `+set` to see all the available values.
        **Examples**: ```bash
        +set
        +set log_channel #logs
        ```
        """
        embed = list_commands_under_group(ctx, self._set)
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
            'Successfully enabled logging in this guild/server.\nMake sure bot has the necessary permissions for the same also setup a log channel using the `set` command.'
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

    @_set.command(
        name='log_channel',
        aliases=['lc'],
        brief='Set the log channel to be used for logging.'
    )
    async def set_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the logging channel using this command.**
        **Examples**: ```bash
        +set log_channel #logs
        +set lc #log-channel
        +set log_channel 757236604690628609
        ```
        """
        await self._set_config_value(
            ctx,
            'log_channel',
            channel.id,
            f'Successfully set `{channel.name}` as a logging channel.\nMake sure the bot has permissions to create and send webhooks in that channel.'
        )

    @_set.command(
        name='prefix',
        brief='Set the prefix to be used by the bot.'
    )
    async def set_prefix(self, ctx, prefix):
        """**You can set the bot prefix using this command.**
        **Examples**: ```bash
        +set prefix !
        +set prefix +
        +set prefix j!
        ```
        """
        await set_custom_prefix(
            self.guilds_collection,
            ctx.guild.id,
            prefix
        )

        embed = normal_embed(
            ctx,
            title='Set prefix',
            description=f'Successfully set `{prefix}` as the bot prefix.\nYou can change it back later.'
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Config(bot))
