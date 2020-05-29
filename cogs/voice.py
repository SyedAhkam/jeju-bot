from discord.ext import commands

import lavalink

class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        #if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            #bot.lavalink = lavalink.Client(bot.user.id)
            #bot.lavalink.add_node('localhost', 2333, 'youshallnotpass', 'eu',
                                  #'music-node')  # Host, Port, Password, Region, Name
            #bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        #lavalink.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(name='join', help='Make the bot join a voice channel you\'re in.')
    async def join(self, ctx):

        if not ctx.author.voice:
            await ctx.send('Please join a voice channel first.')
            return

        channel = ctx.author.voice.channel

        await channel.connect()

    @commands.command(name='leave', help='Make the bot leave a voice channel it currently is in.')
    async def leave(self, ctx):

        guild = ctx.guild
        voice_client =guild.voice_client

        if not voice_client:
            await ctx.send('Bot isn\'t connected to any VoiceChannel.')
            return

        await voice_client.disconnect()

    @commands.command(name='play', help='Play anything from youtube.')
    async def play(self, ctx, *, url):
        guild = ctx.guild
        voice_client = guild.voice_client

        player = await voice_client.create_ytdl_player(url)
        player.start()

def setup(bot):
    bot.add_cog(Voice(bot))
