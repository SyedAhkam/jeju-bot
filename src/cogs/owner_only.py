from discord.ext import commands

class OwnerOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """This applies a check to all the commands under this cog"""
        is_owner = await self.bot.is_owner(ctx.author)
        if not is_owner:
            raise commands.NotOwner()
            return
        return True

    @commands.command(
        name='load',
        brief='Loads a specified category.'
    )
    async def load(self, ctx, extension):
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded Successfully.')

    @commands.command(
        name='unload',
        brief='Unloads a specified category.'
    )
    async def unload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded Successfully.')

    @commands.command(
        name='reload',
        brief='Reloads a specified category.'
    )
    async def reload(self, ctx, extension):
        ctx.bot.unload_extension(f'cogs.{extension}')
        ctx.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} reloaded Successfully.')

def setup(bot):
    bot.add_cog(OwnerOnly(bot))
