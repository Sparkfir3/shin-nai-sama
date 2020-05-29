import discord

import players

import asyncio
import sys
sys.path.append('source/data')
from dictionaries import channels
from dictionaries import start_role_messages
from dictionaries import game_messages
from enums import Game_Phase

sys.path.append('source/utility')
from misc import get_dm_channel
from misc import get_participant_role
from misc import get_dead_role
import confirmations

game_phase = Game_Phase.Null
day_number = 0
end_setup = True

participant_role = None
dead_role = None

# Sets up the game and starts it
async def on_start(user, fallback_channel):
    global channels
    await on_reset()

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
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "There are not enough players to properly run the game without errors. Failed to start the game.")
        await fallback_channel.send(embed = embed)
        return

    try:
        global game_phase
        game_phase = Game_Phase.Starting

        # Distribute roles
        players.Player_Manager.distribute_roles()
        dm = await get_dm_channel(user)
        await dm.send(embed = players.Player_Manager.list_players_with_roles())

        # Confirm roles
        await asyncio.sleep(1)
        message = await fallback_channel.send("Roles have been distributed, and have been privately sent to {}. Are you okay with this role distribution?".format(user.display_name))
        await confirmations.confirm_roles(fallback_channel, message, user)

    except Exception as inst:
        on_reset()
        embed = discord.Embed(color = 0xff0000, title = "Error in Starting Game", description = "There was an error in starting the game:\n{}.".format(inst))
        await fallback_channel.send(embed = embed)

# Called after user confirms role distribution
async def continue_start(channel):
    await asyncio.sleep(0.5)
    try:
        async with channel.typing():
            # Send start message
            meeting_hall = channels["meeting"]
            await meeting_hall.send(game_messages["start"])

            # DM players
            await dm_roles()
            await channel.send("Humans, monkeys, and the crow have been sent their roles.")

            # Close channels
            everyone = channels["meeting"].guild.default_role
            await channels["meeting"].set_permissions(everyone, read_messages = True, send_messages = False)
            await channels["wolves"].set_permissions(everyone, read_messages = False, send_messages = False)
            await channels["snake"].set_permissions(everyone, read_messages = False, send_messages = False)
            await channels["spider"].set_permissions(everyone, read_messages = False, send_messages = False)

            # Setup channels
            await asyncio.sleep(0.5)
            await setup_channels_perms(channel)

            # Give players role
            global participant_role, dead_role
            participant_role = await get_participant_role()
            dead_role = await get_dead_role()
            for player in players.Player_Manager.players:
                await player.user.add_roles(participant_role)
                await asyncio.sleep(0.1)


            await channel.send("The first morning will start in 5 minutes.\nUse the `$next` command to skip the timer and start the first morning.")

        # Timer
        global end_setup
        end_setup = False
        timer = 0
        max_timer = 5 * 60
        while not end_setup:
            await asyncio.sleep(1)
            timer += 1
            if timer >= max_timer:
                end_setup = True
        await channel.send("**GAME IS STARTING**")
        await asyncio.sleep(2)

        # TODO - force exit game using reset command
        # Run game
        while True:
            await morning()
            await asyncio.sleep(1)
            # Check win condition

            await day()
            await asyncio.sleep(1)
            # Check win condition

            await evening()
            await asyncio.sleep(1)

            await night()
            await asyncio.sleep(1)

        # End game

    # Error
    except Exception as inst:
        await on_reset()
        embed = discord.Embed(color = 0xff0000, title = "Game Crashed", description = "There was an error in the game:\n{}.\n\nThe game has been forcefully reset.".format(inst))
        await channel.send(embed = embed)

async def dm_roles():
    await asyncio.sleep(1)

    # DM players - humans
    for player in players.Player_Manager.humans:
        dm = await get_dm_channel(player.user)
        await dm.send(start_role_messages["human"])
    await asyncio.sleep(0.1)

    # DM players - monkeys
    dm = await get_dm_channel(players.Player_Manager.monkeys[0].user)
    await dm.send(start_role_messages["monkey"].format(players.Player_Manager.monkeys[1].name))
    await asyncio.sleep(0.1)
    
    dm = await get_dm_channel(players.Player_Manager.monkeys[1].user)
    await dm.send(start_role_messages["monkey"].format(players.Player_Manager.monkeys[0].name))
    await asyncio.sleep(0.1)
    
    # DM players - crow    
    dm = await get_dm_channel(players.Player_Manager.crow.user)
    await dm.send(start_role_messages["crow"])
    await asyncio.sleep(0.1)

    # DM badger
    if players.Player_Manager.badger != None:
        dm = await get_dm_channel(players.Player_Manager.badger.user)
        await dm.send(start_role_messages["human"])
        await asyncio.sleep(0.1)

async def setup_channels_perms(channel):
    global channels

    # Wolves
    mention_wolves = ""
    for wolf in players.Player_Manager.wolves:
        await channels["wolves"].set_permissions(wolf.user, read_messages = True, send_messages = False)
        mention_wolves += "{} ".format(wolf.user.mention)
        await asyncio.sleep(0.5)
    await asyncio.sleep(1)
    await channels["wolves"].send("{}\n\n{}".format(mention_wolves.strip(), start_role_messages["wolves"]))

    await asyncio.sleep(0.5)
    await channel.send("Wolves have been setup.")

    # Snake
    await channels["snake"].set_permissions(players.Player_Manager.snake.user, read_messages = True, send_messages = False)
    await asyncio.sleep(1)
    await channels["snake"].send("{}\n\n{}".format(players.Player_Manager.snake.user.mention, start_role_messages["snake"]))

    await asyncio.sleep(0.5)
    await channel.send("Snake has been setup.")

    # Spider
    await channels["spider"].set_permissions(players.Player_Manager.spider.user, read_messages = True, send_messages = False)
    await asyncio.sleep(1)
    await channels["spider"].send("{}\n\n{}".format(players.Player_Manager.spider.user.mention, start_role_messages["spider"]))

    await asyncio.sleep(0.5)
    await channel.send("Spider has been setup.")

# ---------------------------------------------------------------------------------

async def morning():
    await asyncio.sleep(0.5)
    global day_number
    day_number += 1

    meeting_hall = channels["meeting"]
    global participant_role
    # First monrning
    if day_number == 1:
        await meeting_hall.send(game_messages["first_morning"].format(participant_role.mention, len(players.Player_Manager.wolves)))

    # Other mornings
    else:
        await meeting_hall.send(game_messages["morning_no_dead"].format(participant_role.mention))

    # Open meeting hall
    for player in players.Player_Manager.players:
        await channels["meeting"].set_permissions(player.user, read_messages = True, send_messages = True)
        # Open voice chat

async def day():
    await asyncio.sleep(1000)

async def evening():
    None

async def night():
    None

# ---------------------------------------------------------------------------------

# Called by the reset command
async def reset_game(ctx):
    await on_reset()
    await ctx.send("Game has been reset.")

# Resets the game; called whenever a reset is needed
async def on_reset():
    global game_phase, day_number, end_setup, participant_role, dead_role
    game_phase = Game_Phase.Null
    day_number = 0
    end_setup = True

    participant_role = None
    dead_role = None

    # Remove players from channels
    try:
        await channels["meeting"].edit(sync_permissions = True)
        await channels["wolves"].edit(sync_permissions = True)
        await channels["snake"].edit(sync_permissions = True)
        await channels["spider"].edit(sync_permissions = True)
    except:
        None

    players.Player_Manager.reset()