import discord

import players

import sys
sys.path.append('source/data')
from dictionaries import channels

sys.path.append('source/utility')
from misc import get_dm_channel

async def on_start(user, fallback_channel):
    global channels
    if channels["moderator"] != None:
        players.Player_Manager.distribute_roles()
        dm = await get_dm_channel(user)

        await dm.send(embed = players.Player_Manager.list_players_with_roles())
        await channels["moderator"].send("Roles have been distributed, and have been privately sent to {}.".format(user.display_name))

    else:
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "The channels have not been setup. Failed to start the game.")
        await fallback_channel.send(embed = embed)
