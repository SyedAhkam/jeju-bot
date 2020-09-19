from discord import Embed
from datetime import datetime

colors = {
    'normal': 0x3c5cac,
    'error': 0xff033e
}

def normal_embed(ctx, title=Embed.Empty, description=Embed.Empty):
    """An embed for common use"""
    embed = Embed(
        description=description,
        color=colors['normal'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=title, icon_url=ctx.bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    return embed

def error_embed(ctx, error_name=Embed.Empty, error_msg=Embed.Empty):
    """An embed for use when handling errors"""
    embed = Embed(
        description=error_msg,
        color=colors['error'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=error_name, icon_url=ctx.bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    return embed
