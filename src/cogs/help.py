from discord.ext import commands
from discord.ext.menus import MenuPages, ListPageSource
from utils.embeds import normal_embed, error_embed
from inspect import cleandoc

class HelpMainMenu(ListPageSource):
    """This is the main menu for help command"""
    def __init__(self, ctx, data):
        super().__init__(data, per_page=10)
        self.ctx = ctx

    async def write_page(self, menu, categories):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        menu_embed = normal_embed(
            self.ctx,
            title='Help!',
            description=cleandoc(
                f"""Hi, Thanks for inviting the bot!
                Tip: Do `{self.ctx.prefix}help <category or command_name>` to get more info about them!
                Examples: ```
                {self.ctx.prefix}help
                {self.ctx.prefix}help info
                {self.ctx.prefix}help ping
                ```
                """
            )
        )
        menu_embed.set_thumbnail(url=self.ctx.guild.icon_url if self.ctx.guild else self.ctx.author.avatar_url)

        menu_embed.set_footer(
            text=f"Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} categories.",
            icon_url=self.ctx.author.avatar_url
        )

        for category in categories:
            menu_embed.add_field(name=category[0], value=category[1], inline=False)

        return menu_embed

    async def format_page(self, menu, entries):
        categories = []
        for entry in entries:
            categories.append((
                entry.qualified_name,
                entry.description if entry.description else 'No description set.'
            ))
        return await self.write_page(menu, categories)

class HelpCogMenu(ListPageSource):
    """This is the menu for showing info about a cog or category"""
    def __init__(self, ctx, data, usage_formatter_func):
        super().__init__(data, per_page=10)
        self.ctx = ctx
        self.usage_formatter_func = usage_formatter_func

    async def write_page(self, menu, commands):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        menu_embed = normal_embed(
            self.ctx,
            title='Help!',
            description=cleandoc(
                f"""Hi, Here you can see all the available commands under this category.
                Tip: Do `{self.ctx.prefix}help <command_name>` to get more info on a command!
                """
            )
        )
        menu_embed.set_thumbnail(url=self.ctx.guild.icon_url if self.ctx.guild else self.ctx.author.avatar_url)

        menu_embed.set_footer(
            text=f"Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.",
            icon_url=self.ctx.author.avatar_url
        )

        for command in commands:
            menu_embed.add_field(name=command[0], value=command[1], inline=False)

        return menu_embed

    async def format_page(self, menu, entries):
        commands = []
        for entry in entries:
            commands.append((
                entry.short_doc or "No Help Message",
                self.usage_formatter_func(self.ctx, entry)
            ))
        return await self.write_page(menu, commands)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignored_cogs = [
            'ErrorHandler',
            'Help',
            'Events',
            'OwnerOnly',
            'Eval'
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
        embed.set_thumbnail(url=ctx.guild.icon_url if ctx.guild else self.ctx.author.avatar_url)

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
    async def help(self, ctx, category_or_command=None):
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
