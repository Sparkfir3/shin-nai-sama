import discord
from discord.ext import commands
from discord.utils import get

# Import main modules
import players

# Import enums
import sys
sys.path.append('Source Code/enums')
import player_types
import game_phases

import asyncio

# ---------------------------------------------------------------------------------------

# Bot setup
client = commands.Bot(command_prefix = '$')
client.remove_command("help")

# Console output on ready
@client.event
async def on_ready():
    print("\n\n\nWe have loggined in as {0.user}\n".format(client))

# ---------------------------------------------------------------------------------------

@client.group(pass_context = True)
async def help(ctx):
    if ctx.invoked_subcommand is None:
        # Regular commands
        description = "$help - Lists all available bot comamnds."
        description += "\n" + "$ping - Test command that gives the bot\'s latency time."

        embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Commands", description = description)
        await ctx.send(embed = embed)

        # Moderator commands
        if check_perms(ctx):
            description = "$add - Adds all given mentioned players to the game."
            description += "\n" + "$remove - Removes all given mentioned players from the game."
            description += "\n" + "$listplayers - Lists all players currently in the game."
            description += "\n" + "$clearplayers - Removes all players from the game."

            description += "\n\n" + "$start - Starts the game."

            embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Moderator Commands", description = description)
            await ctx.send(embed = embed)

        # Dev commands
            show_dev_commands = True
            if show_dev_commands:
                description = "$bypasslimit - Toggles the player limit of 12 for the game on and off."

                embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Dev Commands", description = description)
                await ctx.send(embed = embed)

@client.command(pass_context = True)
async def ping(ctx):
	await ctx.send(":ping_pong: Pong! Latency: {} ms".format(round(client.latency, 1)))

# ---------------------------------------------------------------------------------------

# Player management
@client.command(pass_context = True, aliases = ["add"])
async def addplayer(ctx):
    # Add player(s)
    names_str = ""
    for i, user in enumerate(ctx.message.mentions):
        # Convert mentioned player into player class
        new_player = players.Player(user, player_types.Player_Types.Human)

        # Attempt to add player
        if players.Player_Manager.add_player(new_player):
            # Format name for output string
            names_str += "`{}`".format(new_player.name)
            if len(ctx.message.mentions) > 1 and i == len(ctx.message.mentions) - 2:
                names_str += " and "
            elif i < len(ctx.message.mentions) - 2:
                names_str += ", "

    # No players given
    if names_str == "":
        await ctx.send("No valid players given.")
    # Valid players added to list
    else:
        await ctx.send("Added {} to list of players.\nThere are now {} players.".format(names_str, len(players.Player_Manager.players)))

# ------------

@client.command(pass_context = True, aliases = ["remove"])
async def removeplayer(ctx):
    await ctx.send(players.Player_Manager.remove_player(ctx.message.mentions))

@client.command(pass_context = True)
async def listplayers(ctx):
    await ctx.send(embed = players.Player_Manager.list_players())

@client.command(pass_context = True)
async def clearplayers(ctx):
    await ctx.send(players.Player_Manager.clear_players())

# ---------------------------------------------------------------------------------------

# Global Variables
bypass_player_limit = True
start_confirm_message = None
start_confirm_user = None

# -------------------

@client.command(pass_context = True)
async def start(ctx):
    # Can't start if waiting for confirmation
    global start_confirm_message
    if not start_confirm_message == None:
        embed = discord.Embed(color = 0xff0000, title = "Awaiting Confirmation", description = "Already waiting on confirmation for game start.")
        await ctx.send(embed = embed)
        return
    # TODO - Can't start if game is in progress
    if False:
        embed = discord.Embed(color = 0xff0000, title = "Game in Progress", description = "The game is already in progress!")
        await ctx.send(embed = embed)
        return

    # Check permission
    if check_perms(ctx):
        number_of_players = len(players.Player_Manager.players)
        global bypass_player_limit

        # Valid number of players
        if number_of_players >= 12:
            embed = discord.Embed(color = 0x00ff00, title = "Start Game", description = "Start the game?".format(number_of_players))
            await confirm_game_start(ctx, embed)

        # Confirm if player limit should be ignored
        elif bypass_player_limit:
            embed = discord.Embed(color = 0x0080ff, title = "Not Enough Players", description = "There are only {} out of the standard minimum of 12 players in the game, are you sure you want to begin?".format(number_of_players))
            await confirm_game_start(ctx, embed)

        # Not enough players
        else:
            embed = discord.Embed(color = 0xff0000, title = "Not Enough Players", description = "There are only {} out of the minimum of 12 players in the game.".format(number_of_players))
            await ctx.send(embed = embed)
    
    # Insufficient permission
    else:
        await ctx.send(embed = insufficient_perms())

# Asks if the user wants to start the game
async def confirm_game_start(ctx, embed):
    global start_confirm_message
    local_confirm_message = await ctx.send(embed = embed)
    start_confirm_message = local_confirm_message
    start_confirm_user = ctx.message.author
    await add_confirm_reactions(local_confirm_message)
    # on_reaction_add event handles yes/no answer

    # Timeout if user has not reacted in time (10 seconds)
    await asyncio.sleep(10)
    if local_confirm_message.id == start_confirm_message.id:
        start_confirm_message = None
        embed = discord.Embed(color = 0xff0000, title = "Timeout - Game Start", description = "Game start has been cancelled due to timing out.")
        await ctx.send(embed = embed)

# ---------------

async def on_start():
    False

# ---------------

@client.command(pass_context = True)
async def bypasslimit(ctx):
    if check_perms(ctx):
        global bypass_player_limit
        bypass_player_limit = not bypass_player_limit
        await ctx.send("Player limit has been {}.".format("disabled" if bypass_player_limit else "enabled"))
    else:
        await ctx.send(embed = insufficient_perms())

# ---------------------------------------------------------------------------------------

# TODO - morning

# ---------------------------------------------------------------------------------------

# TODO - start and end day phase

# ---------------------------------------------------------------------------------------

# TODO - lynching

# ---------------------------------------------------------------------------------------

# TODO - start and end evening

# ---------------------------------------------------------------------------------------

# TODO - start and end night

# ---------------------------------------------------------------------------------------

# TODO - kill players & yeet command

# ---------------------------------------------------------------------------------------

# TODO - end game

# ---------------------------------------------------------------------------------------

# Permissions
def check_perms(ctx):
    id = discord.utils.get(ctx.guild.roles, name="Moderator")
    if id in ctx.author.roles:
        return True
    return False

# TODO - check if moderator is included in reactions
def react_contains_mod(reaction):
    return True

def insufficient_perms():
	description = "You do not have permission to use this command."
	embed = discord.Embed(color = 0xff0000, title = "Insufficient Permissions", description = description)
	return embed

# ---------------------------------------------------------------------------------------

async def add_confirm_reactions(message):
    await message.add_reaction('✅')
    await message.add_reaction('❌')

def react_yes(reaction):
    return reaction.emoji == '✅'

def react_no(reaction):
    return reaction.emoji == '❌'

# ---------------------------------------------------------------------------------------

@client.event
async def on_reaction_add(reaction, user):
    # Do nothing if the message wasn't from the bot OR if there is only 1 reaction (bot's reaction)
    if not reaction.message.author.bot or reaction.count == 1:
        return
    #await reaction.message.channel.send("Test")

    channel = reaction.message.channel

    # Start confirmation
    global start_confirm_message
    if reaction.message.id == start_confirm_message.id and react_contains_mod(reaction):
        if react_yes(reaction): # ✅
            start_confirm_message = None
            await on_start()

        elif react_no(reaction): # ❌
            start_confirm_message = None
            embed = discord.Embed(color = 0xff0000, title = "Game Start Cancelled", description = "Game start has been cancelled.")
            await channel.send(embed = embed)
        return

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def test(ctx):
    message = await ctx.send("Ree")
    await add_confirm_reactions(message)

    # try:
    #     reaction, user = await client.wait_for('reaction_add', timeout=2)
    # except:
    #     await ctx.send("Fuck")

    # def check(reaction, user):
    #         return user == message.author and str(reaction.emoji) == '👍'

    #     try:
    #         reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    #     except asyncio.TimeoutError:
    #         await channel.send('👎')
    #     else:
    #         await channel.send('👍')

# ---------------------------------------------------------------------------------------

# Access code removed for security purposes
client.run("")