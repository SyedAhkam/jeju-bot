from discord import Embed
from datetime import datetime

colors = {
    'normal': 0x3c5cac,
    'error': 0xff033e
}

def normal_embed(title=Embed.Empty, description=Embed.Empty):
    """An embed for common use"""
    return Embed(title=title, description=description, color=colors['normal'])

def error_embed(ctx, error_name=Embed.Empty, error_msg=Embed.Empty):
    """An embed for use when handling errors"""
    embed = Embed(description=error_msg, color=colors['error'])
    embed.set_author(name=error_name, icon_url=ctx.bot.user.avatar_url)
    return embed
