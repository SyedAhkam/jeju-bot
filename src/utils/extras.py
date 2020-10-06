from exceptions import ApiFetchError
from utils.embeds import normal_embed

import asyncio
import json

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

async def send_webhook(webhook_url, session, content, username, embeds=[]):
    """Sends a webhook to the specified url."""
    payload = {}
    payload['content'] = content
    payload['username'] = username
    payload['embeds'] = embeds

    async with session.post(
        webhook_url,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'},
        raise_for_status=True
    ) as response:
        return response

async def ask__yes_or_no_question(ctx, bot, embed_title, question, deny_message, timeout_message):
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
