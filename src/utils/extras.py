from exceptions import ApiFetchError
from utils.embeds import normal_embed
from discord import Webhook, AsyncWebhookAdapter

import asyncio


async def fetch_json(url, session):
    """Fetch json content from a url."""
    async with session.get(url) as response:
        if not response.status == 200:
            raise ApiFetchError(status=response.status)
        return await response.json()


async def fetch_text(url, session):
    """Fetch text content from a url."""
    async with session.get(url) as response:
        if not response.status == 200:
            raise ApiFetchError(status=response.status)
        return await response.text()


async def send_webhook(url, session, *args, **kwargs):
    """Sends a webhook to the specified url."""
    webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
    await webhook.send(*args, **kwargs)


async def ask_yes_or_no_question(ctx, bot, embed_title, question, deny_message, timeout_message):
    """Ask a yes or no question using the wait_for feature."""
    def check(msg):
        return msg.content.lower().split()[0] in ['yes', 'no', 'y', 'n'] and msg.channel == ctx.channel and msg.author == ctx.author

    embed = normal_embed(
        ctx,
        title=embed_title,
        description=question
    )
    await ctx.send(embed=embed)

    try:
        user_response_msg = await bot.wait_for('message', check=check, timeout=60.0)

        if user_response_msg.content.lower().split()[0] in ['no', 'n']:
            await ctx.send(deny_message)
            return False

        return True

    except asyncio.TimeoutError:
        await ctx.send(timeout_message)
        return False
