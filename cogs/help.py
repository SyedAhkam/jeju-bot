from discord.ext import commands

from discord.ext.menus import MenuPages, ListPageSource

import discord
import datetime

def format(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])

    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"`qwq {cmd_and_aliases} {params}`"

class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        super().__init__(data, per_page=5)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        menu_embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xfacaf5)
        menu_embed.set_author(name='Help', url=discord.Embed.Empty, icon_url=self.ctx.bot.user.avatar_url)
        menu_embed.set_thumbnail(url=self.ctx.guild.icon_url)

        menu_embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            menu_embed.add_field(name=name, value=value, inline=False)

        return menu_embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.help or "No description", format(entry)))
        return await self.write_page(menu, fields)

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    async def cmd_help(self, ctx, command, help_embed):
        formatted = format(command)
        name = command.name
        help = command.help
        cog = command.cog_name

        help_embed.description = f'{formatted}\nCog:{cog}\n{help}'

        await ctx.send(embed=help_embed)

    @commands.command(name='help', help='Shows this message')
    async def help(self, ctx, *, command_or_cog=None):

        help_embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xfacaf5)
        help_embed.set_author(name='Help', url=discord.Embed.Empty, icon_url=ctx.bot.user.avatar_url)
        help_embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=discord.Embed.Empty)
        help_embed.set_thumbnail(url=ctx.guild.icon_url)

        if command_or_cog:
            cog = ctx.bot.get_cog(command_or_cog)
            command = ctx.bot.get_command(command_or_cog)

            if cog:
                if len(cog.get_commands()) < 1:
                    await ctx.send('No commands in this cog.')
                    return
                menu = MenuPages(source=HelpMenu(ctx, list(cog.get_commands())), delete_message_after=True, timeout=60.0)
                await menu.start(ctx)
                return

            if command:
                await self.cmd_help(ctx, command, help_embed)
                return
            await ctx.send(f'No command or cog found by the name ``{command_or_cog}``')
            return


        menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
                             delete_message_after=True,
                             timeout=60.0)
        await menu.start(ctx)


def setup(bot):
    bot.add_cog(Help(bot))
