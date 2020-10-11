from discord.ext import commands
from utils.extras import fetch_json, ask_yes_or_no_question
from utils.embeds import normal_embed

import random


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
        self._8ball_responses = [
            'As I see it, yes.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'It is certain.',
            'It is decidedly so.',
            'Most likely.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Outlook good.',
            'Reply hazy, try again.',
            'Signs point to yes.',
            'Very doubtful.',
            'Without a doubt.',
            'Yes.',
            'Yes- definitely.',
            'You may rely on it.'
        ]

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
        """**Fetches a random meme from reddit.**
        **Examples**: ```bash
        +meme
        +memes
        ```
        """
        json_response = await fetch_json(self.memeapi_base_url, self.bot.aio_session)

        if json_response['nsfw']:
            user_choice = await ask_yes_or_no_question(
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

    @commands.command(
        name='roll',
        aliases=['dice', 'rd'],
        brief='Simulates a dice roll.'
    )
    async def roll(self, ctx, number_of_dice: int = 1, number_of_sides: int = 6):
        """**Rolls a dice for you.**
        **Args**:
        - `number_of_dice`: The number of dices you want to roll. The default is 1.
        - `number_of_sides`: The number of sides you want each dice to have. The default is 6.
        **Examples**: ```bash
        +roll
        +roll 2
        +roll 5 10
        ```
        """
        if number_of_dice > 10:
            await ctx.send('Please keep the number of dices less than 10.')
            return

        if number_of_sides > 100:
            await ctx.send('Please keep the number of sides less than 100.')
            return

        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for dice in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(
        name='8ball',
        aliases=['ball', '8b'],
        brief='Ask a yes or no question to 8ball.'
    )
    async def _8ball(self, ctx, *, question):
        """**Ask a question to the magic 8ball.**
        **Args**:
        - `question`: The question to ask the 8ball.
        **Examples**: ```bash
        +8ball Is jeju the best bot ever?
        +8ball Will I be single forever?
        +8ball Am I a good coder? 
        ```
        """
        responses = self._8ball_responses

        choosen_response = random.choice(responses)

        embed = normal_embed(
            ctx,
            title='8ball'
        )

        embed.add_field(name='You asked:', value=question, inline=False)
        embed.add_field(
            name='Magic 8ball thinks:',
            value=choosen_response,
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
