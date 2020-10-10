from discord.ext import commands
from utils.extras import send_webhook
from utils.db import get_config_value
from utils.embeds import log_embed_danger, log_embed_warn, log_embed_info

import textwrap
import ago


class Logging(commands.Cog):
    """Everything related to logging."""

    def __init__(self, bot):
        self.bot = bot
        self.config_collection = bot.db.config

    async def _get_webhook(self, guild):
        is_logging_enabled = await get_config_value(
            self.config_collection,
            guild.id,
            'is_logging_enabled'
        )
        if not is_logging_enabled:
            return None

        logging_channel_id = await get_config_value(
            self.config_collection,
            guild.id,
            'log_channel'
        )
        if not logging_channel_id:
            return None
        logging_channel_obj = guild.get_channel(logging_channel_id)

        all_webhooks = await logging_channel_obj.webhooks()
        if not all_webhooks:
            avatar = await self.bot.user.avatar_url.read()
            webhook = await logging_channel_obj.create_webhook(
                name='Jeju Logging',
                avatar=avatar,
                reason='Jeju bot logging'
            )
            return webhook

        for webhook in all_webhooks:
            if webhook.name == 'Jeju Logging':
                return webhook

        avatar = await self.bot.user.avatar_url.read()
        webhook = await logging_channel_obj.create_webhook(
            name='Jeju Logging',
            avatar=avatar,
            reason='Jeju bot logging'
        )
        return webhook

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message:
            return

        if not message.content:
            return

        webhook = await self._get_webhook(message.guild)
        if not webhook:
            return

        embed = log_embed_danger(
            'Message Deleted',
            self.bot
        )
        embed.add_field(name='Author:', value=message.author.name, inline=True)
        embed.add_field(name='Channel:',
                        value=message.channel.name, inline=True)
        embed.add_field(name='Content:', value=message.content, inline=False)

        embed.set_footer(
            text=f'Message ID: {message.id}', icon_url=message.author.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        webhook = await self._get_webhook(messages[0].guild)
        if not webhook:
            return

        available_space_per_message = 2048 / len(messages)
        description = ''
        for message in messages:
            to_be_added = f'**By {message.author}**: {message.content}'
            shortened_message = textwrap.shorten(
                to_be_added, width=available_space_per_message)
            description += f'{shortened_message}\n'

        embed = log_embed_danger(
            'Bulk Messages Deleted(Purged)',
            self.bot,
            description=description
        )
        embed.set_footer(text=f'{len(messages)} messages deleted',
                         icon_url=messages[0].author.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if not (message_before.content == message_after.content):
            webhook = await self._get_webhook(message_after.guild)
            if not webhook:
                return

            embed = log_embed_warn(
                'Message Edited',
                self.bot
            )
            embed.add_field(
                name='Before:', value=message_before.content, inline=False)
            embed.add_field(
                name='After:', value=message_after.content, inline=False)

            embed.set_footer(
                text=f'Message ID: {message_after.id}', icon_url=message_after.author.avatar_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        webhook = await self._get_webhook(channel.guild)
        if not webhook:
            return

        embed = log_embed_danger(
            'Channel deleted',
            self.bot
        )
        embed.add_field(name='Name:', value=channel.name, inline=True)
        embed.add_field(name='Type:', value=channel.type, inline=True)
        embed.add_field(name='Category:', value=channel.category, inline=True)

        embed.set_footer(text=f'Channel ID: {channel.id}')

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        webhook = await self._get_webhook(channel.guild)
        if not webhook:
            return

        embed = log_embed_info(
            'Channel created',
            self.bot
        )
        embed.add_field(name='Name:', value=channel.name, inline=True)
        embed.add_field(name='Type:', value=channel.type, inline=True)
        embed.add_field(name='Category:', value=channel.category, inline=True)

        embed.set_footer(text=f'Channel ID: {channel.id}')

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, channel_before, channel_after):
        webhook = await self._get_webhook(channel_after.guild)
        if not webhook:
            return

        embed = log_embed_warn(
            'Channel updated',
            self.bot
        )

        if not (channel_before.name == channel_after.name):
            embed.add_field(
                name='Name:', value=channel_before.name, inline=True)
            embed.add_field(
                name='Name Changed:', value=f'**Before**: {channel_before.name}\n**After**: {channel_after.name}', inline=False)

            embed.set_footer(text=f'Channel ID: {channel_after.id}')

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return
        if str(channel_after.type) == 'text':
            if not (channel_before.topic == channel_after.topic):
                embed.add_field(
                    name='Name:', value=channel_before.name, inline=True)
                embed.add_field(
                    name='Topic Changed:', value=f'**Before**: {channel_before.topic}\n**After**: {channel_after.topic}', inline=False)

                embed.set_footer(text=f'Channel ID: {channel_after.id}')

                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

                return
            if not (channel_before.overwrites == channel_after.overwrites):
                # TODO: list the perms modified

                role_or_member = list(channel_after.overwrites)[0]
                embed.add_field(
                    name='Name:', value=channel_before.name, inline=True)
                embed.add_field(name='Permission overwrites updated:',
                                value=f'Permission overwrites updated for `{role_or_member.name}`', inline=False)

                embed.set_footer(text=f'Channel ID: {channel_after.id}')

                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        webhook = await self._get_webhook(member.guild)
        if not webhook:
            return

        embed = log_embed_info(
            'Member joined',
            self.bot
        )
        embed.add_field(name='Name:', value=member.name, inline=True)
        embed.add_field(name='Mention:', value=member.mention, inline=True)
        embed.add_field(name='Joined Discord:', value=ago.human(
            member.created_at), inline=True)

        embed.set_footer(
            text=f'Member ID: {member.id}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        webhook = await self._get_webhook(member.guild)
        if not webhook:
            return

        embed = log_embed_danger(
            'Member left',
            self.bot
        )
        embed.add_field(name='Name:', value=member.name, inline=True)
        embed.add_field(name='Mention:', value=member.mention, inline=True)
        embed.add_field(name='Joined Discord:', value=ago.human(
            member.created_at), inline=True)
        embed.add_field(name='Roles:', value=', '.join(
            [role.mention for role in member.roles]), inline=False)

        embed.set_footer(
            text=f'Member ID: {member.id}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_member_update(self, member_before, member_after):
        webhook = await self._get_webhook(member_after.guild)
        if not webhook:
            return

        embed = log_embed_warn(
            'Member update',
            self.bot
        )

        if not (member_before.nick == member_after.nick):
            # nickname change
            embed.add_field(name='Name:', value=member_after.name, inline=True)
            embed.add_field(name='Nickname change:',
                            value=f'**Before**: {member_before.nick}\n**After**: {member_after.nick}', inline=False)

            embed.set_footer(
                text=f'Member ID: {member_after.id}', icon_url=member_after.avatar_url)
            embed.set_thumbnail(url=member_after.avatar_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (member_before.roles == member_after.roles):
            new_roles = [
                role for role in member_after.roles if role not in member_before.roles]
            removed_roles = [
                role for role in member_before.roles if role not in member_after.roles]

            if len(member_before.roles) < len(member_after.roles):
                # added roles
                embed.add_field(
                    name='Name:', value=member_after.name, inline=True)
                embed.add_field(name='Roles added:', value=', '.join(
                    [role.mention for role in new_roles]), inline=False)

                embed.set_footer(
                    text=f'Member ID: {member_after.id}', icon_url=member_after.avatar_url)
                embed.set_thumbnail(url=member_after.avatar_url)

                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

            else:
                # removed roles
                embed.add_field(
                    name='Name:', value=member_after.name, inline=True)
                embed.add_field(name='Roles removed:', value=', '.join(
                    [role.mention for role in removed_roles]), inline=False)

                embed.set_footer(
                    text=f'Member ID: {member_after.id}', icon_url=member_after.avatar_url)
                embed.set_thumbnail(url=member_after.avatar_url)

                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

    @commands.Cog.listener()
    async def on_user_update(self, user_before, user_after):
        all_guilds = self.bot.guilds
        guilds_which_user_shares = [
            guild for guild in all_guilds if user_after in guild.members]

        webhooks = []
        for guild in guilds_which_user_shares:
            webhook = await self._get_webhook(guild)
            if not webhook:
                continue

            webhooks.append(webhook)

        if not webhooks:
            return

        embed = log_embed_warn(
            'User updated',
            self.bot
        )

        if not (user_before.name == user_after.name):
            # username update
            embed.add_field(name='Name:', value=user_after.name, inline=True)
            embed.add_field(name='Username update:',
                            value=f'**Before**: {user_before.name}\n**After**: {user_after.name}', inline=False)

            embed.set_footer(
                text=f'User ID: {user_after.id}', icon_url=user_after.avatar_url)
            embed.set_thumbnail(url=user_after.avatar_url)

            for webhook in webhooks:
                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

            return
        if not (user_before.discriminator == user_after.discriminator):
            # discriminator update
            embed.add_field(name='Name:', value=user_after.name, inline=True)
            embed.add_field(name='Discriminator update:',
                            value=f'**Before**: {user_before.discriminator}\n**After**: {user_after.discriminator}', inline=False)

            embed.set_footer(
                text=f'User ID: {user_after.id}', icon_url=user_after.avatar_url)
            embed.set_thumbnail(url=user_after.avatar_url)

            for webhook in webhooks:
                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

            return
        if not (user_before.avatar == user_after.avatar):
            # avatar update
            embed.add_field(name='Name:', value=user_after.name, inline=True)
            embed.add_field(
                name='Avatar update:', value=f'**Before**: {user_before.avatar_url}\n**After**: {user_after.avatar_url}', inline=False)

            embed.set_footer(
                text=f'User ID: {user_after.id}', icon_url=user_after.avatar_url)
            embed.set_thumbnail(url=user_after.avatar_url)

            for webhook in webhooks:
                await send_webhook(
                    webhook.url,
                    self.bot.aio_session,
                    embed=embed
                )

            return

    @commands.Cog.listener()
    async def on_guild_update(self, guild_before, guild_after):
        webhook = await self._get_webhook(guild_after)
        if not webhook:
            return

        embed = log_embed_warn(
            'Guild update',
            self.bot
        )

        if not (guild_before.name == guild_after.name):
            # name update
            embed.add_field(name='Name:', value=guild_after.name, inline=True)
            embed.add_field(
                name='Name update:', value=f'**Before**: {guild_before.name}\n**After**: {guild_after.name}', inline=False)

            embed.set_footer(
                text=f'Guild ID: {guild_after.id}', icon_url=guild_after.icon_url)
            embed.set_thumbnail(url=guild_after.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (guild_before.region == guild_after.region):
            # region update
            embed.add_field(name='Name:', value=guild_after.name, inline=True)
            embed.add_field(
                name='Region update:', value=f'**Before**: {guild_before.region}\n**After**: {guild_after.region}', inline=False)

            embed.set_footer(
                text=f'Guild ID: {guild_after.id}', icon_url=guild_after.icon_url)
            embed.set_thumbnail(url=guild_after.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (guild_before.icon == guild_after.icon):
            # icon update
            embed.add_field(name='Name:', value=guild_after.name, inline=True)
            embed.add_field(
                name='Icon update:', value=f'**Before**: {guild_before.icon_url}\n**After**: {guild_after.icon_url}', inline=False)

            embed.set_footer(
                text=f'Guild ID: {guild_after.id}', icon_url=guild_after.icon_url)
            embed.set_thumbnail(url=guild_after.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (guild_before.owner == guild_after.owner):
            # ownership update
            embed.add_field(name='Name:', value=guild_after.name, inline=True)
            embed.add_field(
                name='Ownership update:', value=f'**Before**: {guild_before.owner.name}\n**After**: {guild_after.owner.name}', inline=False)

            embed.set_footer(
                text=f'Guild ID: {guild_after.id}', icon_url=guild_after.icon_url)
            embed.set_thumbnail(url=guild_after.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (guild_before.verification_level == guild_after.verification_level):
            # verification_level update
            embed.add_field(name='Name:', value=guild_after.name, inline=True)
            embed.add_field(
                name='Verification level update:', value=f'**Before**: {guild_before.verification_level}\n**After**: {guild_after.verification_level}', inline=False)

            embed.set_footer(
                text=f'Guild ID: {guild_after.id}', icon_url=guild_after.icon_url)
            embed.set_thumbnail(url=guild_after.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_info(
            'Role created',
            self.bot
        )

        embed.add_field(name='Name:', value=role.name, inline=True)
        embed.add_field(name='Hoisted:', value=role.hoist, inline=True)
        embed.add_field(name='Color:', value=role.color, inline=True)

        embed.set_footer(
            text=f'Role ID: {role.id}', icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_danger(
            'Role deleted',
            self.bot
        )

        embed.add_field(name='Name:', value=role.name, inline=True)
        embed.add_field(name='Hoisted:', value=role.hoist, inline=True)
        embed.add_field(name='Color:', value=role.color, inline=True)

        embed.set_footer(
            text=f'Role ID: {role.id}', icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before, role_after):
        guild = role_after.guild
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_warn(
            'Role updated',
            self.bot
        )

        if not (role_before.name == role_after.name):
            # name update
            embed.add_field(name='Name:', value=role_after.name, inline=True)
            embed.add_field(
                name='Name update:', value=f'**Before**: {role_before.name}\n**After**: {role_after.name}', inline=False)

            embed.set_footer(
                text=f'Role ID: {role_after.id}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (role_before.hoist == role_after.hoist):
            # hoist update
            embed.add_field(name='Name:', value=role_after.name, inline=True)
            embed.add_field(
                name='Hoist update:', value=f'**Before**: {role_before.hoist}\n**After**: {role_after.hoist}', inline=False)

            embed.set_footer(
                text=f'Role ID: {role_after.id}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (role_before.mentionable == role_after.mentionable):
            # mentionable update
            embed.add_field(name='Name:', value=role_after.name, inline=True)
            embed.add_field(
                name='Mentionable update:', value=f'**Before**: {role_before.mentionable}\n**After**: {role_after.mentionable}', inline=False)

            embed.set_footer(
                text=f'Role ID: {role_after.id}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (role_before.color == role_after.color):
            # color update
            embed.add_field(name='Name:', value=role_after.name, inline=True)
            embed.add_field(
                name='Color update:', value=f'**Before**: {role_before.color}\n**After**: {role_after.color}', inline=False)

            embed.set_footer(
                text=f'Role ID: {role_after.id}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

            return

        if not (role_before.permissions == role_after.permissions):
            # permissions update
            # TODO: do this uh why am i being so lazy
            return

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, emojis_before, emojis_after):
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_warn(
            'Emojis updated',
            self.bot
        )

        new_emojis = [
            emoji for emoji in emojis_after if emoji not in emojis_before]
        removed_emojis = [
            emoji for emoji in emojis_before if emoji not in emojis_after]

        if len(emojis_before) < len(emojis_after):
            # new emojis
            embed.add_field(name='Emojis Added:', value=', '.join(
                [str(emoji) for emoji in new_emojis]), inline=False)

            embed.set_footer(
                text=f'Total emojis: {len(emojis_after)}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

        else:
            # emojis got removed
            embed.add_field(name='Emojis Deleted:', value=', '.join(
                [str(emoji) for emoji in removed_emojis]), inline=False)

            embed.set_footer(
                text=f'Total emojis: {len(emojis_after)}', icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)

            await send_webhook(
                webhook.url,
                self.bot.aio_session,
                embed=embed
            )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member_or_user):
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_danger(
            'Member Banned',
            self.bot
        )
        embed.add_field(name='Name:', value=member_or_user.name, inline=True)
        embed.add_field(name='Roles:', value=', '.join(
            [role.mention for role in member_or_user.roles]), inline=False)

        embed.set_footer(
            text=f'User ID: {member_or_user.id}', icon_url=member_or_user.avatar_url)
        embed.set_thumbnail(url=member_or_user.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        webhook = await self._get_webhook(guild)
        if not webhook:
            return

        embed = log_embed_info(
            'Member Unbanned',
            self.bot
        )
        embed.add_field(name='Name:', value=user.name, inline=True)

        embed.set_footer(
            text=f'User ID: {user.id}', icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        await send_webhook(
            webhook.url,
            self.bot.aio_session,
            embed=embed
        )


def setup(bot):
    bot.add_cog(Logging(bot))
