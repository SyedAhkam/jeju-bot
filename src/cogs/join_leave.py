from discord.ext import commands
from utils.db import get_config_value

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_roles_collection = bot.db.auto_roles
        self.config_collection = bot.db.config
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # is_auto_roles_enabled = await get_config_value(
        #     self.auto_roles_collection,
        #     member.guild.id,
        #     'is_auto_roles_enabled'
        # )
        # FIXME
        is_auto_roles_enabled = await self.config_collection.find_one({
            'guild_id': member.guild.id,
            'config_type': 'is_auto_roles_enabled'
        })

        if not is_auto_roles_enabled:
            return

        roles_docs = await self.auto_roles_collection.find({'guild_id': member.guild.id}).to_list(None)

        roles_objs = []
        for doc in roles_docs:
            role_obj = member.guild.get_role(doc['_id'])
            roles_objs.append(role_obj)

        await member.add_roles(*roles_objs)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # TODO
        pass

def setup(bot):
    bot.add_cog(JoinLeave(bot))