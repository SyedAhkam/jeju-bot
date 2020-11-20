from discord.ext.menus import ListPageSource
from utils.embeds import normal_embed
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
                f"""**Hi, what can I help you with?**
                ▫️ For more specific and detailed help for each commands, use:
                `{self.ctx.prefix}help [category | command_name]`
                ▫️  For further help, join my support server.
                **Bot Prefix**: {self.ctx.prefix}
                """
            )
        )
        menu_embed.set_thumbnail(
            url=self.ctx.guild.icon_url if self.ctx.guild else self.ctx.author.avatar_url)

        menu_embed.set_footer(
            text=f"Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} categories.",
            icon_url=self.ctx.author.avatar_url
        )

        for category in categories:
            menu_embed.add_field(
                name=f'🔹 {category[0].capitalize()}', value=category[1], inline=False)

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
                f"""**Hi, These are all the available commands under this category.**
                ▫️ For more specific and detailed help for each commands, use:
                `{self.ctx.prefix}help [category | command_name]`
                """
            )
        )
        menu_embed.set_thumbnail(
            url=self.ctx.guild.icon_url if self.ctx.guild else self.ctx.author.avatar_url)

        menu_embed.set_footer(
            text=f"Showing {offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.",
            icon_url=self.ctx.author.avatar_url
        )

        for command in commands:
            menu_embed.add_field(
                name=f'🔹 {command[0]}', value=command[1], inline=False)

        return menu_embed

    async def format_page(self, menu, entries):
        commands = []
        for entry in entries:
            commands.append((
                entry.short_doc or "No Help Message",
                self.usage_formatter_func(self.ctx, entry)
            ))
        return await self.write_page(menu, commands)
