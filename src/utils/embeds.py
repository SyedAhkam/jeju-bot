from discord import Embed
from datetime import datetime

colors = {
    'normal': 0x3c5cac,
    'error': 0xff033e,
    'warn': 0xe3e05a
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


def normal_embed_using_message(message, bot, title=Embed.Empty, description=Embed.Empty):
    """Similar to normal_embed but for use when ctx is not available."""
    embed = Embed(
        description=description,
        color=colors['normal'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=title, icon_url=bot.user.avatar_url)
    embed.set_footer(text=message.author.name,
                     icon_url=message.author.avatar_url)
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


def list_commands_under_group(ctx, group):
    """Returns an embed listing all the commands inside a group."""
    description = ''
    for command in group.commands:
        to_be_added = f'**{command.name}** - {command.brief}\n'
        description += to_be_added

    return normal_embed(ctx, 'Available choices', description)


def log_embed_info(title, bot, description=Embed.Empty):
    """An embed for use in logging with a level of info."""
    embed = Embed(
        description=description,
        color=colors['normal'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=title, icon_url=bot.user.avatar_url)
    return embed


def log_embed_warn(title, bot, description=Embed.Empty):
    """An embed for use in logging with a level of warn."""
    embed = Embed(
        description=description,
        color=colors['warn'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=title, icon_url=bot.user.avatar_url)
    return embed


def log_embed_danger(title, bot, description=Embed.Empty):
    """An embed for use in logging with a level of danger or critical."""
    embed = Embed(
        description=description,
        color=colors['error'],
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=title, icon_url=bot.user.avatar_url)
    return embed


def is_embed(object):
    if isinstance(object, Embed):
        return True
    else:
        False
