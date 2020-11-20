from discord.ext import commands
from discord.ext.menus import MenuPages
from menus.help import HelpMainMenu, HelpCogMenu
from utils.embeds import error_embed, normal_embed, is_embed


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            verify_checks=False,
            command_attrs={
                'name': 'help',
                'aliases': ['h']
            }
        )
        self.ignored_cogs = [
            'ErrorHandler',
            'Help',
            'Events',
            'OwnerOnly',
            'Eval',
            'BotCheck',
            'Jishaku',
            'Logging',
            'JoinLeave'
        ]

    @staticmethod
    def format_command_usage(ctx, command):
        """Format command usages to show aliases and params"""
        cmd_and_aliases = "|".join([str(command), *command.aliases])

        params = []
        for key, value in command.params.items():
            if key not in ("self", "ctx"):
                params.append(f"[{key}]" if "NoneType" in str(
                    value) else f"<{key}>")

        params = " ".join(params)

        return f"`{ctx.prefix}{cmd_and_aliases} {params}`"

    async def send_bot_help(self, mapping):
        all_cogs = list(mapping.keys())

        cogs_filtered = [
            cog for cog in all_cogs if cog and (cog.qualified_name not in self.ignored_cogs)]

        menu = MenuPages(
            source=HelpMainMenu(
                self.context,
                cogs_filtered
            ),
            clear_reactions_after=True,
            timeout=60.0
        )
        await menu.start(self.context)

    async def send_cog_help(self, cog):
        all_cog_commands = cog.get_commands()
        filtered_commands = await self.filter_commands(all_cog_commands)

        if not filtered_commands:
            embed = error_embed(
                self.context,
                error_name='No Commands',
                error_msg=f'Sorry, There are no commands in this category yet.\nMaybe check out other categories by using just `{self.context.prefix}help`.'
            )
            await self.context.send(embed=embed)
            return

        menu = MenuPages(
            source=HelpCogMenu(
                self.context,
                filtered_commands,
                self.format_command_usage
            ),
            clear_reactions_after=True,
            timeout=60.0
        )
        await menu.start(self.context)

    async def send_group_help(self, group):
        embed = normal_embed(
            self.context,
            title='Help!',
            description=(group.help or "No Help Message") +
            "\n▫️ *This command is a group.*"
        )
        embed.set_thumbnail(
            url=self.context.guild.icon_url if self.context.guild else self.context.author.avatar_url)

        embed.add_field(name='🔹 __**Name**__:',
                        value=group.name, inline=False)
        embed.add_field(name='🔹 __**Category**__:',
                        value=group.cog.qualified_name, inline=False)
        embed.add_field(name='🔹 __**Aliases**__:', value=', '.join(
            group.aliases) or 'None', inline=True)

        embed.add_field(
            name='🔹 __**Usage**__:',
            value=self.format_command_usage(self.context, group),
            inline=False
        )

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = normal_embed(
            self.context,
            title='Help!',
            description=command.help or "No Help Message"
        )
        embed.set_thumbnail(
            url=self.context.guild.icon_url if self.context.guild else self.context.author.avatar_url)

        embed.add_field(name='🔹 __**Name**__:',
                        value=command.name, inline=False)
        embed.add_field(name='🔹 __**Category**__:',
                        value=command.cog.qualified_name, inline=False)
        embed.add_field(name='🔹 __**Aliases**__:', value=', '.join(
            command.aliases) or 'None', inline=True)

        embed.add_field(name='🔹 __**Usage**__:', value=self.format_command_usage(
            self.context, command), inline=False)

        await self.context.send(embed=embed)

    async def command_not_found(self, string):
        embed = error_embed(
            self.context,
            error_name='No Command or Category',
            error_msg=f'Sorry, There\'s no command or category by the name: `{string}`\nYou should check out just ``{self.context.prefix}help``.'
        )
        return embed

    async def subcommand_not_found(self, command, string):
        embed = error_embed(
            self.context,
            error_name='No SubCommand',
            error_msg=f'Sorry, There\'s no subcommand by the name: `{string}` under `{command.name}` command.\nYou should check out just ``{self.context.prefix}{command.name}``.'
        )
        return embed

    async def send_error_message(self, error):
        if is_embed(error):
            await self.context.send(embed=error)
        else:
            await self.context.send(error)
