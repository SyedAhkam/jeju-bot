from discord.ext import commands
from utils.embeds import error_embed
import exceptions


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignored = (commands.CommandNotFound)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Using on_command_error as an error handler."""
        error = getattr(error, 'original', error)

        if isinstance(error, self.ignored):
            return

        if isinstance(error, exceptions.AdminPermsRequiredError):
            embed = error_embed(
                ctx,
                error_name='Admin Perms Required',
                error_msg='Sorry, This command requires admin perms to execute.'
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, exceptions.UserBlacklistedError):
            if error.global_:
                embed = error_embed(
                    ctx,
                    error_name='Blacklisted',
                    error_msg='Sorry, You\'ve been blacklisted from using any of my commands globally.\nPlease stop trying to use them.'
                )
                await ctx.send(embed=embed)
            else:
                embed = error_embed(
                    ctx,
                    error_name='Blacklisted',
                    error_msg='Sorry, You\'ve been blacklisted from using any of my commands in this server.\nPlease stop trying to use them.'
                )
                await ctx.send(embed=embed)

            return

        if isinstance(error, exceptions.ApiFetchError):
            embed = error_embed(
                ctx,
                error_name='API Fetch Error',
                error_msg='Sorry, Failed to fetch data from an external API.\nMaybe try again later.'
            )
            await ctx.send(embed=embed)

        if isinstance(error, commands.DisabledCommand):
            embed = error_embed(
                ctx,
                error_name='Disabled Command',
                error_msg='Sorry, This command has been disabled by the owner of bot.\nPlease stop trying to use it.'
            )
            await ctx.send(embed=embed)
            return

        # Im a little confused about this error
        if isinstance(error, commands.ConversionError):
            embed = error_embed(
                ctx,
                error_name='Conversion Error',
                error_msg='Sorry, I failed to convert your input.\nMaybe the command expects a number and you provided a text instead?'
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.NoPrivateMessage):
                embed = error_embed(
                    ctx,
                    error_name='No Private Message',
                    error_msg='Sorry, This command can\'t be used in private messages.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.PrivateMessageOnly):
                embed = error_embed(
                    ctx,
                    error_name='Private Message Only',
                    error_msg='Sorry, This command can only be used in private messages.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.NotOwner):
                embed = error_embed(
                    ctx,
                    error_name='Not Owner',
                    error_msg='Sorry, This command can only be used by the owner of bot.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.MissingPermissions):
                required_perms = ', '.join(error.missing_perms)
                embed = error_embed(
                    ctx,
                    error_name='Missing Permmisions',
                    error_msg=f'Sorry, You need to have these permissions to run this command: ``{required_perms}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.BotMissingPermissions):
                required_perms = ', '.join(error.missing_perms)
                embed = error_embed(
                    ctx,
                    error_name='Bot Missing Permmisions',
                    error_msg=f'Sorry, I need to have these permissions to run this command: ``{required_perms}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.MissingRole):
                missing_role = ctx.guild.get_role(error.missing_role)
                embed = error_embed(
                    ctx,
                    error_name='Missing Role',
                    error_msg=f'Sorry, You need to have this role to run this command: ``{missing_role.name}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.BotMissingRole):
                missing_role = ctx.guild.get_role(error.missing_role)
                embed = error_embed(
                    ctx,
                    error_name='Bot Missing Role',
                    error_msg=f'Sorry, I need to have this role to run this command: ``{missing_role.name}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.MissingAnyRole):
                missing_roles_list = []
                for role in error.missing_roles:
                    missing_roles_list.append(ctx.guild.get_role(role))
                missing_roles = ', '.join(
                    [role.name for role in missing_roles_list])
                embed = error_embed(
                    ctx,
                    error_name='Missing Any Role',
                    error_msg=f'Sorry, You need to have atleast one of these roles to run this command: ``{missing_roles}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.BotMissingAnyRole):
                missing_roles_list = []
                for role in error.missing_roles:
                    missing_roles_list.append(ctx.guild.get_role(role))
                missing_roles = ', '.join(
                    [role.name for role in missing_roles_list])
                embed = error_embed(
                    ctx,
                    error_name='Bot Missing Any Role',
                    error_msg=f'Sorry, I need to have atleast one of these roles to run this command: ``{missing_roles}``'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.NSFWChannelRequired):
                embed = error_embed(
                    ctx,
                    error_name='NSFW Channel Required',
                    error_msg='Sorry, This channel needs to be a nsfw channel in order to run this command.'
                )
                await ctx.send(embed=embed)
                return

        if isinstance(error, commands.UserInputError):
            if isinstance(error, commands.MissingRequiredArgument):
                embed = error_embed(
                    ctx,
                    error_name='Missing Required Argument',
                    error_msg=f'Sorry, You\'re missing a required argument: ``{error.param.name}``\nMaybe check out the help command?'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.ArgumentParsingError):
                if isinstance(error, commands.UnexpectedQuoteError):
                    embed = error_embed(
                        ctx,
                        error_name='Unexpected Quote Error',
                        error_msg='Sorry, An unexpected quote(") in your input has been detected.\nMaybe check out the help command?'
                    )
                    await ctx.send(embed=embed)
                    return

                if isinstance(error, commands.InvalidEndOfQuotedStringError):
                    embed = error_embed(
                        ctx,
                        error_name='Invalid End Of Quoted String Error',
                        error_msg='Sorry, An empty space was expected after your closing quoted(""<-this) string.\nMaybe check out the help command?'
                    )
                    await ctx.send(embed=embed)
                    return

                if isinstance(error, commands.ExpectedClosingQuoteError):
                    embed = error_embed(
                        ctx,
                        error_name='Expected Closing Quote Error',
                        error_msg='Sorry, You started a quoted("") string, But you never closed it.\nMaybe check out the help command?'
                    )
                    await ctx.send(embed=embed)
                    return

                if isinstance(error, commands.BadArgument):
                    embed = error_embed(
                        ctx,
                        error_name='Bad Argument',
                        error_msg='Sorry, I failed to convert your input.\nMaybe the command expects a number and you provided a text instead?'
                    )
                    await ctx.send(embed=embed)
                    return

                if isinstance(error, commands.BadUnionArgument):
                    # TODO: do this later
                    pass

                if isinstance(error, commands.TooManyArguments):
                    embed = error_embed(
                        ctx,
                        error_name='Too Many Arguments',
                        error_msg='Sorry, You provided too many arguments to this command.\nMaybe check out the help command?'
                    )
                    await ctx.send(embed=embed)
                    return

        if isinstance(error, commands.CommandOnCooldown):
            embed = error_embed(
                ctx,
                error_name='Command On Cooldown',
                error_msg=f'Sorry, This command is on a cooldown.\nPlease wait `{round(error.retry_after, 1)}` more seconds before retrying.'
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.MaxConcurrencyReached):
            # Don't need this for now
            pass

        if isinstance(error, commands.ExtensionError):
            if isinstance(error, commands.ExtensionAlreadyLoaded):
                embed = error_embed(
                    ctx,
                    error_name='Extension Already Loaded',
                    error_msg='Sorry, This Extension is already loaded.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.ExtensionNotLoaded):
                embed = error_embed(
                    ctx,
                    error_name='Extension Not Loaded',
                    error_msg='Sorry, This Extension is not loaded.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.NoEntryPointError):
                embed = error_embed(
                    ctx,
                    error_name='No Entry Point Error',
                    error_msg='Sorry, This Extension does not contain a setup funtion.'
                )
                await ctx.send(embed=embed)
                return

            if isinstance(error, commands.ExtensionFailed):
                embed = error_embed(
                    ctx,
                    error_name='Extension Failed',
                    error_msg='Sorry, This Extension Failed to load.'
                )
                await ctx.send(embed=embed)

            if isinstance(error, commands.ExtensionNotFound):
                embed = error_embed(
                    ctx,
                    error_name='Extension Not Found',
                    error_msg='Sorry, This Extension was not found.'
                )
                await ctx.send(embed=embed)
                return

        if self.bot.is_env_dev():
            await ctx.send(f'```py\n{error.__class__.__name__}: {str(error)}\n```')
            raise error
            return

        embed = error_embed(
            ctx,
            error_name='Unexpected Error',
            error_msg='Sorry, An unexpected error occured.\nThis gotta be a very serious error, Notifying the owner of bot...'
        )
        await ctx.send(embed=embed)

        app_info = await self.bot.application_info()
        ctx_dict = f'```py\n{ctx.__dict__}\n```'
        await app_info.owner.send(f'An error occured in {ctx.guild.id} while invoking command: {ctx.command.name}\n{error.__class__.__name__}: {str(error)}\n{ctx_dict}')
        raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
