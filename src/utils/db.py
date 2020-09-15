async def get_guild(guilds_collection, guild_id):
    """Get a guild from db."""
    return await guilds_collection.find_one({'_id': guild_id})

async def add_guild(guilds_collection, guild):
    """Add a guild to db."""
    await guilds_collection.insert_one({
        '_id': guild.id,
        'guild_name': guild.name,
        'guild_owner_id': guild.owner_id,
        'bot_prefix': '+'
    })

async def remove_guild(guilds_collection, guild_id):
    """Remove a guild from db."""
    await guilds_collection.delete_one({'_id': guild_id})
