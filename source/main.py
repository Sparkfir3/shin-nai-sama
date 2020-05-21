# Import discord
import discord
from discord.ext import commands
from discord.utils import get

# Import python modules
import sys
import asyncio

# Import main modules
import players

sys.path.append("")
from settings import TOKEN

# Import enums
sys.path.append("source/enums")
from player_types import Player_Types
from game_phases import Game_Phase

# ---------------------------------------------------------------------------------------

# Bot setup
client = commands.Bot(command_prefix = '$')
client.remove_command("help")

# Console output on ready
@client.event
async def on_ready():
    print("\n\n\nWe have loggined in as {0.user}\n\n".format(client))

# ---------------------------------------------------------------------------------------

@client.group(pass_context = True)
async def help(ctx):
    if ctx.invoked_subcommand is None:
        # Regular commands
        description = "$help - Lists all available bot comamnds."
        description += "\n" + "$poll - Starts a poll with the given text."
        description += "\n" + "$ping - Test command that gives the bot\'s latency time."

        embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Commands", description = description)
        await ctx.send(embed = embed)

        # Moderator commands
        if check_perms(ctx):
            description = "$add - Adds all given mentioned players to the game."
            description += "\n" + "$remove - Removes all given mentioned players from the game."
            description += "\n" + "$listplayers - Lists all players currently in the game."
            description += "\n" + "$clearplayers - Removes all players from the game."

            description += "\n\n" + "$channel - Sets up the channels for the game. Use `$help channel` for more info."
            description += "\n" + "$storechannels - Stores the channels into a text document for later use."
            description += "\n" + "$loadchannels - Loads the stored channels from the text document for use."
            description += "\n" + "$listchannels - Lists all the channels used for the game and their assigned channels."

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

# Setup Channels
channel_moderator = None
channel_meeting = None
channel_snake = None
channel_spider = None
channel_wolves = None
channel_dead = None

channel_voice_meeting = None
channel_voice_wolves = None

channels = {
    "moderator" : channel_moderator,
    "meeting" : channel_meeting,
    "snake" : channel_snake,
    "spider" : channel_spider,
    "wolves" : channel_wolves,
    "dead" : channel_dead,

    "voice_meeting" : channel_voice_meeting,
    "voice_wolves" : channel_voice_wolves
}

# ------------------

@help.command(pass_context = True, aliases = ["channels"])
async def channel(ctx):
    description = "Text Channels:\n`$channel <channel_name> <channel_mention>`"
    description += "\nSets up the specified text channel as the channel mentioned.\nValid channel names are:"
    description += "\n • moderator"
    description += "\n • meeting"
    description += "\n • snake"
    description += "\n • spider"
    description += "\n • wolves"
    description += "\n • dead"

    description += "\n\nVoice Channels:\n`$channel voice <channel_name> <channel_mention>`"
    description += "\nSets up the specified voice channel as the channel mentioned.\nValid channel names are:"
    description += "\n • meeting"
    description += "\n • wolves"
    description += "\nTo mention a voice channel, use the format `<#channel_id>`, where `channel_id` is the id number of the channel."
    description += "To access the id of a channel, you must be in Discord's development mode."

    embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Command - $channel", description = description)
    await ctx.send(embed = embed)

@client.command(pass_context = True, aliases = ["channels"])
async def channel(ctx, *args):
    global channels
    # Grab arguments
    try:
        arg = args[0].lower()
        text_channel = ctx.message.channel_mentions[0]
    except: # Invalid arguments
        embed = discord.Embed(color = 0xff0000, title = "Invalid Arguments", description = "Invalid arguments supplied.\nUse `$help channel` for more details.")
        await ctx.send(embed = embed)
        return

    # Setup text channel
    if arg in channels:
        try:
            channels[arg] = text_channel
            text = "Successfully setup <#{}> as the {} channel.".format(str(channels[arg].id), arg)
            embed = discord.Embed(color = 0x00ff00, title = "Channel Setup Success", description = text)
            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(color = 0xff0000, title = "Channel Setup Failed", description = "Failed to setup the given channel.")
            await ctx.send(embed = embed)
        return

    # Grab optional argument for voice channels
    try:
        arg_voice = args[1].lower()
    except:
        None

    # Setup voice channel
    if arg == "voice":
        # Meeting voice chat
        if arg_voice == "meeting":
            try:
                channels["voice_meeting"] = text_channel
                text = "Successfully setup <#{}> as the meeting voice channel.".format(str(channels["voice_meeting"].id))
                embed = discord.Embed(color = 0x00ff00, title = "Channel Setup Success", description = text)
                await ctx.send(embed = embed)
            except:
                embed = discord.Embed(color = 0xff0000, title = "Channel Setup Failed", description = "Failed to setup the meeting voice channel.\nUse the format `<#channel_id>` to mention voice channels.")
                await ctx.send(embed = embed)
            return

        # Wolf voice chat
        elif arg_voice == "wolves":
            try:
                channels["voice_wolves"] = text_channel
                text = "Successfully setup <#{}> as the wolves voice channel.".format(str(channels["voice_wolves"].id))
                embed = discord.Embed(color = 0x00ff00, title = "Channel Setup Success", description = text)
                await ctx.send(embed = embed)
            except:
                embed = discord.Embed(color = 0xff0000, title = "Channel Setup Failed", description = "Failed to setup the wolves voice channel.\nUse the format `<#channel_id>` to mention voice channels.")
                await ctx.send(embed = embed)
            return

    # Nothing happened
    embed = discord.Embed(color = 0xff0000, title = "Invalid Arguments", description = "Invalid arguments supplied.\nUse `$help channel` for more details.")
    await ctx.send(embed = embed)

# --------------

@client.command(pass_context = True, aliases = ["storechannel"])
async def storechannels(ctx):
    file = open("channels.txt", 'w')

    global channels
    for channel in channels:
        if channels[channel] == None:
            file.write("None\n")
        else:
            file.write("{}\n".format(str(channels[channel].id)))
    file.close()

    embed = discord.Embed(color = 0x00ff00, title = "Channel Setup Success", description = "Successfully stored channels.")
    await ctx.send(embed = embed)

@client.command(pass_context = True, aliases = ["loadchannel", "readchannels", "readchannel"])
async def loadchannels(ctx):
    file = open("channels.txt", 'r')
    content = file.read()
    text = content.split("\n")
    file.close()
    count = 0

    async with ctx.channel.typing():
        for i, c in enumerate(channels):
            if text[i] != "None":
                try:
                    channels[c] = client.get_channel(int(text[i]))
                    count += 1
                except:
                    await ctx.send("Failed to load the {} channel.".format(c))
            else:
                await ctx.send("There is no {} channel to load.".format(c))

            await asyncio.sleep(0.25)

    if count == 0:
        embed = discord.Embed(color = 0xff0000, title = "Channel Setup Done", description = "Could not load any channels.")
    else:
        embed = discord.Embed(color = 0x00ff00, title = "Channel Setup Done", description = "Successfully loaded {} channels.".format(count))
    await ctx.send(embed = embed)

# -----------------------

@client.command(pass_context = True, aliases = ["listchannel"])
async def listchannels(ctx):
    description = ""

    global channels
    for i, c in enumerate(channels):
        # Text channel
        if i <= 5:
            description += "{} = {}\n".format(c.capitalize(), "<#{}>".format(channels[c].id) if channels[c] != None else "None")

        # Voice channels:
        elif i == 6:
            description += "\nMeeting (Voice) = {}\n".format("<#{}>".format(channels[c].id) if channels[c] != None else "None")
        elif i == 7:
            description += "Wolves (Voice) = {}".format("<#{}>".format(channels[c].id) if channels[c] != None else "None")

    embed = discord.Embed(color = 0x0080ff, title = "Channel List", description = description)
    await ctx.send(embed = embed)

# ---------------------------------------------------------------------------------------

# Player management
@client.command(pass_context = True, aliases = ["add"])
async def addplayer(ctx):
    # Add player(s)
    names_str = ""
    for i, user in enumerate(ctx.message.mentions):
        # Convert mentioned player into player class
        new_player = players.Player(user, Player_Types.Human)

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
            embed = discord.Embed(color = 0x00ff00, title = "Start Game", description = "The following {} players are in the game:\n\n{}\n\nStart the game?".format(number_of_players, players.Player_Manager.list_players_raw()))
            await confirm_game_start(ctx, embed)

        # Confirm if player limit should be ignored
        elif bypass_player_limit:
            embed = discord.Embed(color = 0xffff00, title = "Not Enough Players", description = "There are only {} out of the standard minimum of 12 players in the game:\n\n{}\nThe game may not function properly. Are you sure you want to begin?".format(number_of_players, players.Player_Manager.list_players_raw()))
            await confirm_game_start(ctx, embed)

        # Not enough players
        else:
            embed = discord.Embed(color = 0xff0000, title = "Not Enough Players", description = "There are only {} out of the minimum of 12 players required for the game:\n\n{}".format(number_of_players, players.Player_Manager.list_players_raw()))
            await ctx.send(embed = embed)
    
    # Insufficient permission
    else:
        await ctx.send(embed = insufficient_perms())

# Asks if the user wants to start the game
async def confirm_game_start(ctx, embed):
    global start_confirm_message, start_confirm_user
    local_confirm_message = await ctx.send(embed = embed)
    start_confirm_message = local_confirm_message
    start_confirm_user = ctx.message.author
    await add_confirm_reactions(local_confirm_message)
    # on_reaction_add event handles yes/no answer

    # Timeout if user has not reacted in time (10 seconds)
    await asyncio.sleep(10)
    if local_confirm_message.id == start_confirm_message.id:
        start_confirm_message = None
        start_confirm_user = None
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

@client.command(pass_context = True)
async def poll(ctx):
    text = ctx.message.content.replace("$poll", "").strip()
    embed = discord.Embed(title = "Poll by {}".format(ctx.message.author.display_name), description = text)
    embed.set_thumbnail(url = ctx.message.author.avatar_url)
    await ctx.message.delete()
    message = await ctx.send(embed = embed)

    await message.add_reaction('👍')
    await message.add_reaction('👎')
    await message.add_reaction('🤷')

# ---------------------------------------------------------------------------------------

# Permissions
def check_perms(ctx):
    id = discord.utils.get(ctx.guild.roles, name="Moderator")
    if id in ctx.author.roles:
        return True
    return False

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
    if reaction.message.id == start_confirm_message.id and start_confirm_user == user:
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
    text = ctx.message.content.replace("$test", "").strip()
    await ctx.send(text)

# ---------------------------------------------------------------------------------------

client.run(TOKEN)