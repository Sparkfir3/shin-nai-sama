import discord

import players

import sys
sys.path.append('source/data')
from dictionaries import channels
from dictionaries import start_role_messages
from enums import Game_Phase

sys.path.append('source/utility')
from misc import get_dm_channel

game_phase = Game_Phase.Null

async def on_start(user, fallback_channel):
    global channels

    # Throw error if channels are not setup
    try:
        for i in channels:
            if channels[i] == None:
                raise Exception("Invalid setup.")

    except:
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "The channels have not been setup. Failed to start the game.")
        await fallback_channel.send(embed = embed)
        return

    # Throw error if not enough players
    if len(players.Player_Manager.players) < 7:
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "There are not enough players to properly run the game. Failed to start the game.")
        await fallback_channel.send(embed = embed)
        return

    try:
        # Distribute roles
        players.Player_Manager.distribute_roles()
        dm = await get_dm_channel(user)

        await dm.send(embed = players.Player_Manager.list_players_with_roles())
        await fallback_channel.send("Roles have been distributed, and have been privately sent to {}.".format(user.display_name))

        # DM players - humans
        for player in players.Player_Manager.humans:
            dm = await get_dm_channel(player.user)
            await dm.send(start_role_messages["human"])

        # DM players - monkeys
        dm = await get_dm_channel(players.Player_Manager.monkeys[0].user)
        await dm.send(start_role_messages["monkey"].format(players.Player_Manager.monkeys[1].name))
        
        dm = await get_dm_channel(players.Player_Manager.monkeys[1].user)
        await dm.send(start_role_messages["monkey"].format(players.Player_Manager.monkeys[0].name))
        
        # DM players - power roles
        dm = await get_dm_channel(players.Player_Manager.snake.user)
        await dm.send(start_role_messages["snake"])
        
        dm = await get_dm_channel(players.Player_Manager.spider.user)
        await dm.send(start_role_messages["spider"])
        
        dm = await get_dm_channel(players.Player_Manager.crow.user)
        await dm.send(start_role_messages["crow"])

    except Exception as inst:
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "There was an error in starting the game:\n{}.".format(inst))
        await fallback_channel.send(embed = embed)

async def reset_game(ctx):
    global game_phase
    game_phase = Game_Phase.Null

    await ctx.send("Game has been reset.")