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
        self.auto_roles_collection = bot.db.auto_roles
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
            # BUG: may create more issues in the future
            if ctx.invoked_with in ['help', 'h']:
                return True
            raise commands.CommandOnCooldown(bucket, retry_after)
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
    
    @commands.group(
        name='add',
        brief='Add some configuration values for a specific feature.',
        invoke_without_command=True
    )
    async def _add(self, ctx):
        """**You can add certain values to use in other features of the bot using this command.**
        **Tip**: You can do just `+add` to see all the available values.
        **Examples**: ```bash
        +add
        +add auto_roles @newbie
        ```
        """
        embed = list_commands_under_group(ctx, self._add)
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
    
    @_enable.command(
        name='auto_roles',
        aliases=['ar'],
        brief='Enable the auto_roles feature of the bot.'
    )
    async def enable_auto_roles(self, ctx):
        """**You can enable the auto roles feature of the bot using this command.**
        **Examples**: ```bash
        +enable auto_roles
        +enable ar
        ```
        """
        await self._enable_guild_feature(
            ctx,
            'is_auto_roles_enabled',
            'Successfully enabled auto roles in this guild/server.\nMake sure bot has the necessary permissions for the same also add roles using the `add` command.'
        )

    @_disable.command(
        name='auto_roles',
        aliases=['ar'],
        brief='Disable the auto_roles feature of the bot.'
    )
    async def disable_auto_roles(self, ctx):
        """**You can disable the auto roles feature of the bot using this command.**
        **Examples**: ```bash
        +disable auto_roles
        +disable ar
        ```
        """
        #TODO: delete leftover roles

        await self._disable_guild_feature(
            ctx,
            'is_auto_roles_enabled',
            'Successfully disabled auto roles in this guild/server.\nYou can use the `enable` command to enable it again.'
        )

    @_set.command(
        name='log_channel',
        aliases=['lc'],
        brief='Set the log channel to be used for logging.'
    )
    async def set_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the logging channel using this command.**
        **Args**:
        - `channel`: The channel you want to be set as a log channel.
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
        name='message_log_channel',
        aliases=['mlc'],
        brief='Set the log channel to be used for logging events related to messages.'
    )
    async def set_message_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the message logging channel using this command.**
        **Args**:
        - `channel`: The channel you want to be set as a message log channel.
        **Examples**: ```bash
        +set message_log_channel #message-logs
        +set mlc #message-log-channel
        +set log_channel 757236604690628609
        ```
        """
        await self._set_config_value(
            ctx,
            'message_log_channel',
            channel.id,
            f'Successfully set `{channel.name}` as a message logging channel.\nMake sure the bot has permissions to create and send webhooks in that channel.'
        )
    
    @_set.command(
        name='server_log_channel',
        aliases=['slc'],
        brief='Set the log channel to be used for logging events related to the server/guild.'
    )
    async def set_server_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the server logging channel using this command.**
        **Args**:
        - `channel`: The channel you want to be set as a server log channel.
        **Examples**: ```bash
        +set server_log_channel #server-logs
        +set slc #server-log-channel
        +set server_log_channel 757236604690628609
        ```
        """
        await self._set_config_value(
            ctx,
            'server_log_channel',
            channel.id,
            f'Successfully set `{channel.name}` as a server logging channel.\nMake sure the bot has permissions to create and send webhooks in that channel.'
        )

    @_set.command(
        name='join_leave_log_channel',
        aliases=['jllc'],
        brief='Set the log channel to be used for logging join/leave events.'
    )
    async def set_join_leave_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the join/leave logging channel using this command.**
        **Args**:
        - `channel`: The channel you want to be set as a join/leave log channel.
        **Examples**: ```bash
        +set join_leave_log_channel #join-leave-logs
        +set jllc #join-leave-log-channel
        +set join_leave_log_channel 757236604690628609
        ```
        """
        await self._set_config_value(
            ctx,
            'join_leave_log_channel',
            channel.id,
            f'Successfully set `{channel.name}` as a join/leave logging channel.\nMake sure the bot has permissions to create and send webhooks in that channel.'
        )
    
    @_set.command(
        name='people_log_channel',
        aliases=['plc'],
        brief='Set the log channel to be used for logging people/member events.'
    )
    async def set_member_log_channel(self, ctx, channel: commands.TextChannelConverter):
        """**You can set the people logging channel using this command.**
        **Args**:
        - `channel`: The channel you want to be set as a people log channel.
        **Examples**: ```bash
        +set people_log_channel #people-logs
        +set plc #member-log-channel
        +set people_log_channel 757236604690628609
        ```
        """
        await self._set_config_value(
            ctx,
            'people_log_channel',
            channel.id,
            f'Successfully set `{channel.name}` as a people logging channel.\nMake sure the bot has permissions to create and send webhooks in that channel.'
        )

    @_set.command(
        name='prefix',
        brief='Set the prefix to be used by the bot.'
    )
    async def set_prefix(self, ctx, prefix):
        """**You can set the bot prefix using this command.**
        **Args**:
        - `prefix`: The prefix you want to set.
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

    @_add.command(
        name='auto_roles',
        aliases=['ar'],
        brief='Add roles to be added to a member on join.'
    )
    async def add_auto_roles(self, ctx, roles: commands.Greedy[commands.RoleConverter]):
        """**You can add the roles for auto roles feature using this command.**
        **Args**:
        - `roles`: The roles you want to add.
        **Examples**: ```bash
        +add auto_roles @newbie @members
        +add auto_roles 741364951356276810
        +add ar 741364951356276810
        ```
        """
        if not roles:
            await ctx.send('Please provide atleast one role.')
            return

        for role in roles:
            await self.auto_roles_collection.insert_one({
                '_id': role.id,
                'guild_id': ctx.guild.id
            })
        
        embed = normal_embed(
            ctx,
            title='Done',
            description=f'Successfully added `{len(roles)}` roles for auto roles.'
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Config(bot))
