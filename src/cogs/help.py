from discord.ext import commands
from discord.ext.menus import MenuPages, ListPageSource
from utils.embeds import normal_embed, error_embed
from menus.help import HelpMainMenu, HelpCogMenu
from inspect import cleandoc

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignored_cogs = [
            'ErrorHandler',
            'Help',
            'Events',
            'OwnerOnly',
            'Eval',
            'BotCheck',
            'Jishaku'
        ]

    @staticmethod
    def format_command_usage(ctx, command):
        """Format command usages to show aliases and params"""
        cmd_and_aliases = "|".join([str(command), *command.aliases])

        params = []
        for key, value in command.params.items():
            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

        params = " ".join(params)

        return f"`{ctx.prefix}{cmd_and_aliases} {params}`"

    async def send_cog_help(self, cog, ctx):
        """Send help about a cog or category"""
        commands = cog.get_commands()
        commands_runnable = []
        for command in commands:
            is_runnable = await command.can_run(ctx)
            if is_runnable:
                commands_runnable.append(command)

        if not commands_runnable:
            embed = error_embed(
                ctx,
                error_name='No Commands',
                error_msg=f'Sorry, There are no commands in this category yet.\nMaybe check out other categories by using just `{ctx.prefix}help`.'
            )
            await ctx.send(embed=embed)
            return

        menu = MenuPages(
            source=HelpCogMenu(ctx, commands_runnable, self.format_command_usage),
            clear_reactions_after=True,
            timeout=60.0
        )
        await menu.start(ctx)

    async def send_command_help(self, command, ctx):
        """Send help about a specific command"""
        embed = normal_embed(
            ctx,
            title='Help!',
            description=command.help or "No Help Message"
        )
        embed.set_thumbnail(url=ctx.guild.icon_url if ctx.guild else ctx.author.avatar_url)

        embed.add_field(name='Name:', value=command.name, inline=True)
        embed.add_field(name='Category:', value=command.cog.qualified_name, inline=True)
        embed.add_field(name='Aliases:', value=', '.join(command.aliases) or 'None', inline=True)

        embed.add_field(name='Usage:', value=self.format_command_usage(ctx, command), inline=False)

        await ctx.send(embed=embed)

    @commands.command(
        name='help',
        aliases=['h'],
        brief='Shows this message.'
    )
    async def help(self, ctx, *, category_or_command=None):
        """Shows the help message for the bot."""
        if category_or_command:
            cog = self.bot.get_cog(category_or_command.lower())
            command = self.bot.get_command(category_or_command)

            if cog:
                await self.send_cog_help(cog, ctx)
            elif command:
                await self.send_command_help(command, ctx)
            else:
                embed = error_embed(
                    ctx,
                    error_name='No Command or Category',
                    error_msg=f'Sorry, There\'s no command or category by the name: `{category_or_command}`\nYou should try out just ``{ctx.prefix}help.``'
                )
                await ctx.send(embed=embed)
        else:
            all_cogs = list(self.bot.cogs.values())
            new_cogs = []
            for cog in all_cogs:
                if cog.qualified_name not in self.ignored_cogs:
                    new_cogs.append(cog)

            menu = MenuPages(
                source=HelpMainMenu(ctx, new_cogs),
                clear_reactions_after=True,
                timeout=60.0
            )
            await menu.start(ctx)

def setup(bot):
    bot.add_cog(Help(bot))
