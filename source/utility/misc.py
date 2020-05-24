import discord

async def get_dm_channel(user):
    channel = user.dm_channel
    if channel == None:
        channel = await user.create_dm()
    return channel
