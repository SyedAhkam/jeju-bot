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

async def set_config_value(config_collection, guild_id, config_type, config_value):
    """Set a config value for a specific type and guild."""
    await config_collection.insert_one({
        'guild_id': guild_id,
        'config_type': config_type,
        'config_value': config_value
    })

async def delete_config_value(config_collection, guild_id, config_type):
    """Delete a config value for a specific type and guild."""
    await config_collection.delete_one({
        'guild_id': guild_id,
        'config_type': config_type
    })

async def delete_guild_config_values(config_collection, guild_id):
    """Delete all the config values associated to a guild."""
    await config_collection.delete_many({'guild_id': guild_id})


async def update_config_value(config_collection, guild_id, config_type, config_value):
    """Update a config value of a specific type and guild."""
    await config_collection.update_one(
        {'guild_id': guild_id, 'config_type': config_type},
        {'$set': {'config_value': config_value}}
    )

async def is_config_value_set(config_collection, guild_id, config_type):
    """Check if a config_value is set or not."""
    return await config_collection.count_documents(
        {'guild_id': guild_id, 'config_type': config_type},
        limit=1
    )

async def get_config_value(config_collection, guild_id, config_type):
    """Get a config value for a specific type and guild."""
    doc = await config_collection.find_one({
        'guild_id': guild_id,
        'config_type': config_type
    })

    return doc['config_value']
