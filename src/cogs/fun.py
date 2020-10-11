from discord.ext import commands
from utils.extras import fetch_json, ask__yes_or_no_question
from utils.embeds import normal_embed


class Fun(commands.Cog, name='fun'):
    """Basic commands for you to have fun."""

    def __init__(self, bot):
        self.bot = bot
        self.memeapi_base_url = 'https://meme-api.herokuapp.com/gimme'
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            3,
            5,
            commands.BucketType.user
        )

    async def cog_check(self, ctx):
        bucket = self.cd_mapping.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True

    @commands.command(
        name='meme',
        aliases=['memes'],
        brief='Get a random meme from reddit.'
    )
    async def meme(self, ctx):
        json_response = await fetch_json(self.memeapi_base_url, self.bot.aio_session)

        if json_response['nsfw']:
            user_choice = await ask__yes_or_no_question(
                ctx,
                self.bot,
                'NSFW Warning!',
                'The meme fetched by the api may be considered NSFW.\nWould you like to see it anyways? (yes/no)',
                'Alrighty, I won\'t show it.',
                'Sorry, You didn\'t respond on time. Please try again!'
            )

            if not user_choice:
                return

        embed = normal_embed(
            ctx,
            title='A random meme for you!',
        )

        postlink = json_response['postLink']
        author = json_response['author']
        ups = json_response['ups']

        embed.add_field(
            name='Title:', value=json_response['title'], inline=True)
        embed.add_field(name='Subreddit:',
                        value=json_response['subreddit'], inline=True)
        embed.add_field(name='Postlink:',
                        value=f'[Click me!]({postlink})', inline=True)

        embed.add_field(
            name='Author:', value=json_response['author'], inline=True)
        embed.add_field(name='Upvotes:',
                        value=json_response['ups'], inline=True)
        embed.add_field(name='NSFW:', value=json_response['nsfw'], inline=True)

        embed.set_image(url=json_response['url'])

        embed.set_footer(text='Powered by the meme-api',
                         icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
