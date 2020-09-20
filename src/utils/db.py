async def is_document_exists(collection, id):
    """Determine if a document with a specific id exist in a collection or not"""
    return await collection.count_documents({'_id': id}, limit=1)

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

async def get_custom_prefix(guilds_collection, guild_id):
    """Gets a custom prefix from guild document of a guild."""
    doc = await get_guild(guilds_collection, guild_id)

    return doc['bot_prefix']
