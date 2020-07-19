# Import discord
import discord
from discord.ext import commands
from discord.utils import get

# Import python modules and settings
import sys
import asyncio

sys.path.append("")
from settings import TOKEN
from settings import DEVMODE
from settings import Settings

# Import main modules
import players

# Import enums and dictionaries
sys.path.append("source/data")
from enums import Player_Types
from enums import Game_Phase
from enums import Perm_Level

from dictionaries import confirm_message
from dictionaries import confirm_user
from dictionaries import channels

# Import other utilities
sys.path.append("source/utility")
from permissions import check_perms
from permissions import insufficient_perms
import confirmations
import misc

# Import gameplay stuff
import gameplay

# ---------------------------------------------------------------------------------------

# Bot setup
client = commands.Bot(command_prefix = ('$' if DEVMODE != "TRUE" else "%"))
client.remove_command("help")

# Console output on connect and ready
@client.event
async def on_connect():
    print("\n\n\nConnecting to Discord...")

@client.event
async def on_disconnect():
    print("\nDisconnected from Discord.\n")

@client.event
async def on_ready():
    print("We have loggined in as {0.user}\n\n".format(client))

# ---------------------------------------------------------------------------------------

@client.group(pass_context = True)
async def help(ctx):
    await asyncio.sleep(0.1)

    if ctx.invoked_subcommand is None:
        # Regular commands
        description = "\n" + "`$poll` - Starts a poll with the given text."
        description += "\n" + "`$listplayers` - Lists all players currently in the game."
        embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Commands", description = description)

        description = "\n" + "`$time` - Checks the current time remaining in the day."
        description += "\n" + "`$spectate` - Spectate the game."
        embed.add_field(name = "In-Game Commands", value = description, inline = False)

        description = "\n" + "`$help` - Lists all available bot comamnds."
        description += "\n" + "`$ping` - Test command that gives the bot\'s latency time."
        embed.add_field(name = "Miscellaneous", value = description, inline = False)

        await ctx.send(embed = embed)

        # Moderator commands
        if check_perms(ctx):
            description = "`$gettingstarted` - Provides information on how to use the bot."
            embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Moderator Commands", description = description)

            description = "`$add` - Adds all given mentioned players to the game. \
                \n`$remove` - Removes all given mentioned players from the game. \
                \n`$listplayers` - Lists all players currently in the game. Use `$help listplayers` for more info. \
                \n`$clearplayers` - Removes all players from the game."
            embed.add_field(name = "Player Management", value = description, inline = False)

            description = "`$channel` - Sets up the channels for the game. Use `$help channel` for more info. \
                \n`$storechannels` - Stores the channels into a text document for later use."
            embed.add_field(name = "Channel Management", value = description, inline = False)

            description = "`$settings` - Displays and sets up settings for the game. Use `$help settings` for more info. \
                \n`$start` - Starts the game. \
                \n`$next` - Skips to the next phase of the game, if possible. \
                \n`$end` - Forcefully ends the game. Players remain in the game, with their roles. \
                \n`$reset` - Forcefully ends and resets the game. Removes all players from the game."
            embed.add_field(name = "Game Management", value = description, inline = False)

            description = "`$kill` - Kills the given player. Can only kill 1 player at a time. \
                \n`$pause` - Pause/unpauses the game timer."
            embed.add_field(name = "Running the Game", value = description, inline = False)

            description = "`$timer` - Starts a timer for a specified amount of minutes. \
                \n`$clearchat` - Removes a specified number of messages from the channel. Defaults to 100."
            embed.add_field(name = "Miscellaneous", value = description, inline = False)

            await ctx.send(embed = embed)

            # Dev commands - only displays for developer
            if ctx.author.id == 221115928933302272:
                description = "`$test` - Test command for testing purposes. \
                    \n`$loadchannels` - Loads the stored channels from the text document for use. \
                    \n`$listchannels` - Lists all the channels used for the game and their assigned channels. \
                    \n`$bypasslimit` - Toggles the player limit of 12 for the game on and off. \
                    \n`$allowdupes` - Toggles whether or not duplicate players are allowed. \
                    \n`$quickstart` - Quickly sets up the game for testing."

                embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Dev Commands", description = description)
                await ctx.send(embed = embed)

@client.command(pass_context = True)
async def gettingstarted(ctx):
    await asyncio.sleep(0.1)

    if check_perms(ctx):
        description = "To start, you first must set up the channels for the game. See `$help channels` for more information. \
            To check if the channels have already been setup, use the `$listchannels` command. \
            \
            \n\nTo add players to the game, use the `$add` command, followed by mentions of the players you wish to add. \
            \n\nOnce all the desired players are added, use the `$start` command to start the game, which will automatically distribute roles and set everything up."
        embed = discord.Embed(color = 0x555555, title = "Getting Started with Shin'nai-sama", description = description)

        # -----

        description = "Once the game is started, a timer will automatically run each phase of the game and open and close channels. \
            \nYou can use the `$next` command to manually skip a phase, if you wish. \
            \nUse the `$kill` command to kill off players. \
            \nThe `$end` command will forcefully quit the game. This is important, as the game *will not automatically end itself*."
        embed.add_field(name = "Running the Game", value = description, inline = False)

        # -----

        description = "There is a `$poll` command that players can use to start polls, and a `$timer` command for moderators to use to create manual timers if needed."
        embed.add_field(name = "Miscallaneous", value = description, inline = False)

        await ctx.send(embed = embed)

    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True)
async def ping(ctx):
    await asyncio.sleep(0.1)
    await ctx.send("🏓 Pong! Latency: {} ms".format(round(client.latency, 1)))

# ---------------------------------------------------------------------------------------

# Dev commands
allow_duplicate_players = False
@client.command(pass_context = True, aliases = ["allowdupes", "enabledupes"])
async def allowduplicates(ctx):
    await asyncio.sleep(0.1)
    # Only Sparkfire can use this command
    if check_perms(ctx) and ctx.author.id == 221115928933302272:
        global allow_duplicate_players
        allow_duplicate_players = not allow_duplicate_players
        await ctx.send("Duplicate players have been {}.".format("enabled" if allow_duplicate_players else "disabled"))

bypass_player_limit = False
@client.command(pass_context = True)
async def bypasslimit(ctx):
    await asyncio.sleep(0.1)
    # Only Sparkfire can use this command
    if check_perms(ctx) and ctx.author.id == 221115928933302272:
        global bypass_player_limit
        bypass_player_limit = not bypass_player_limit
        await ctx.send("Player limit has been {}.".format("disabled" if bypass_player_limit else "enabled"))

@client.command(pass_context = True)
async def quickstart(ctx):
    await asyncio.sleep(0.1)
    # Only Sparkfire can use this command
    if check_perms(ctx) and ctx.author.id == 221115928933302272:
        global bypass_player_limit
        bypass_player_limit = True
        global allow_duplicate_players
        allow_duplicate_players = True
        
        async with ctx.channel.typing():
            await loadchannels(ctx)
            await asyncio.sleep(0.1)
            if len(ctx.message.mentions) > 0:
                await asyncio.sleep(0.1)
                for i in range(8):
                    await addplayer(ctx)

            await asyncio.sleep(0.5)

        await start(ctx)

# ---------------------------------------------------------------------------------------

# Settings - Help
@help.command(pass_context = True, aliases = ["setting"])
async def settings(ctx):
    await asyncio.sleep(0.1)

    description = "Displays and sets up various settings for the game."
    embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Command - $settings", description = description)

    description = "`$settings wolf <value>` \
    \nSets the number of wolves that will appear. `<value>` must be either auto` or a positive number. `auto` sets the wolf count to 1 for every 4 players, rounded down."
    embed.add_field(name = "Badger", value = description, inline = False)

    description = "`$settings badger <value>` \
    \nSets the chance of the badger appearing. `<value>` must be a number between 0 and 100, inclusive."
    embed.add_field(name = "Badger", value = description, inline = False)

    description = "`$settings monkey <value>` \
    \nToggles whether or not the monkeys appear. `<value>` must be either `true` or `false`."
    embed.add_field(name = "Monkeys", value = description, inline = False)

    await ctx.send(embed = embed)

# Settings - Display
@client.group(pass_context = True, aliases = ["setting"])
async def settings(ctx):
    await asyncio.sleep(0.1)

    if ctx.invoked_subcommand is None:
        await ctx.send(embed = Settings.get_settings_embed())

# Settings - Set
@settings.command(pass_context = True, aliases = ["wolf"])
async def wolves(ctx, *args):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
        try:
            value = args[0]

            # Check "auto"
            try:
                if value.lower() == "auto" or value.lower() == "automatic":
                    Settings.wolf_count = 0
                    await ctx.send("Wolf count set to automatic (1 per 4 players).")
                    return
            except:
                None
            
            # Set value
            value = int(value[0])
            if value > 0:
                Settings.wolf_count = value
                await ctx.send("Wolf count set to {}.".format(value))
            else:
                raise Exception("Invalid argument.") 

        except:
            await ctx.send("Please enter a valid argument: either `auto` or a positive number.")

    # Invalid permission
    else:
        await insufficient_perms(ctx)

@settings.command(pass_context = True)
async def badger(ctx, *args):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
        try:
            value = int(args[0])
            if value >= 0 and value <= 100:
                Settings.badger_chance = value
                await ctx.send("Badger chance set to {}%".format(value))

            else:
                raise Exception("Invalid argument.") 

        except:
            await ctx.send("Please enter a valid argument: a number between 0 and 100, inclusive.")

    # Invalid permission
    else:
        await insufficient_perms(ctx)

@settings.command(pass_context = True, aliases = ["monkeys"])
async def monkey(ctx, *args):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
        try:
            if args[0].lower() == "true":
                Settings.monkeys_enabled = True
                await ctx.send("Monkeys have been enabled.")

            elif args[0].lower() == "false":
                Settings.monkeys_enabled = False
                await ctx.send("Monkeys have been disabled.")

            else:
                raise Exception("Invalid argument.") 

        except:
            await ctx.send("Please enter a valid argument: either \"true\" or \"false\".")

    # Invalid permission
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

# Setup Channels
@help.command(pass_context = True, aliases = ["channels"])
async def channel(ctx):
    await asyncio.sleep(0.1)
    embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Command - $channel", description = "")

    description = "`$channel <channel_name> <channel_mention>` \
    \nSets up the specified text channel as the channel mentioned.\nValid channel names are: \
    \n • moderator \
    \n • meeting \
    \n • snake \
    \n • spider \
    \n • wolves \
    \n • dead"
    embed.add_field(name = "Text Channels", value = description, inline = False)

    description = "\n`$channel voice <channel_name> <channel_mention>` \
    \nSets up the specified voice channel as the channel mentioned.\nValid channel names are: \
    \n • meeting \
    \n • wolves \
    \nTo mention a voice channel, use the format `<#channel_id>`, where `channel_id` is the ID number of the channel.  \
    To access and copy the ID of a channel, you must be in Discord's developer mode."
    embed.add_field(name = "Voice Channels", value = description, inline = False)

    await ctx.send(embed = embed)

@client.command(pass_context = True, aliases = ["channels"])
async def channel(ctx, *args):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
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

    # Invalid permission
    else:
        await insufficient_perms(ctx)

# --------------

@client.command(pass_context = True, aliases = ["storechannel"])
async def storechannels(ctx):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
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

    # Insufficient perms
    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True, aliases = ["loadchannel", "readchannels", "readchannel"])
async def loadchannels(ctx):
    # Check permissions
    if check_perms(ctx):
        try:
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

        # Failed to load
        except:
            embed = discord.Embed(color = 0xff0000, title = "Error Loading Channels", description = "There was an error in loading the channels. \
                \nThis may occur if channels have never been previously stored before.")
            await ctx.send(embed = embed)

    # Insufficient perms
    else:
        await insufficient_perms(ctx)

# -----------------------

@client.command(pass_context = True, aliases = ["listchannel"])
async def listchannels(ctx):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx):
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

    # Insufficient perms
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

# Player management
@client.command(pass_context = True, aliases = ["add"])
async def addplayer(ctx):
    await asyncio.sleep(0.1)

    # Check if game is running
    if gameplay.game_phase > Game_Phase.Null:
        description = "Cannot edit players while the game is in progress."
        embed = discord.Embed(color = 0xff0000, title = "Cannot Edit Players", description = description)
        await ctx.send(embed = embed)

    # Check permission
    elif check_perms(ctx):
        # Add player(s)
        names_str = ""
        global allow_duplicate_players
        for i, user in enumerate(ctx.message.mentions):
            # Convert mentioned player into player class
            new_player = players.Player(user, Player_Types.Human)

            # Attempt to add player
            if players.Player_Manager.add_player(new_player, allow_dupes = allow_duplicate_players):
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
            length = len(players.Player_Manager.players)
            await ctx.send("Added {} to the list of players.\nThere {} now {} player{}.".format(names_str, \
                "are" if length > 1 else "is", \
                length, \
                "s" if length > 1 else ""))

    # Insufficient Perms
    else:
        await insufficient_perms(ctx)

# ------------

@client.command(pass_context = True, aliases = ["removeplayers", "remove"])
async def removeplayer(ctx):
    await asyncio.sleep(0.1)

    # Check if game is running
    if gameplay.game_phase > Game_Phase.Null:
        description = "Cannot edit players while the game is in progress."
        embed = discord.Embed(color = 0xff0000, title = "Cannot Edit Players", description = description)
        await ctx.send(embed = embed)

    # Check permissions
    elif check_perms(ctx):
        await ctx.send(players.Player_Manager.remove_player(ctx.message.mentions))
    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True)
async def clearplayers(ctx):
    await asyncio.sleep(0.1)

    # Check if game is running
    if gameplay.game_phase > Game_Phase.Null:
        description = "Cannot edit players while the game is in progress."
        embed = discord.Embed(color = 0xff0000, title = "Cannot Edit Players", description = description)
        await ctx.send(embed = embed)

    # Check permissions
    elif check_perms(ctx):
        await ctx.send(players.Player_Manager.clear_players())
    else:
        await insufficient_perms(ctx)

# ------------

@help.command(pass_context = True)
async def listplayers(ctx):
    await asyncio.sleep(0.1)

    description = "`$listplayers` \
    \nLists all players currently assigned to the game. Separates between alive and dead players. \
    \
    \n\n`$listplayers mention` \
    \nMentions all players currently assigned to the game. Requires administrator-level permissions. \
    \n\n`$listplayers roles` \
    \
    \nLists all players currently assigned to the game with their roles. Requires administrator-level permissions."

    embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Command - $listplayers", description = description)
    await ctx.send(embed = embed)

@client.command(pass_context = True)
async def listplayers(ctx, *args):
    await asyncio.sleep(0.1)

    if len(args) > 0:
        # Mention players
        if args[0].lower() == "mention":
            if check_perms(ctx):
                await ctx.send(players.Player_Manager.list_players_raw(mention = True))
            else:
                await insufficient_perms(ctx)

        # List with roles
        elif args[0].lower() == "roles" or args[0].lower() == "role":
            if check_perms(ctx):
                await ctx.send(embed = players.Player_Manager.list_players_with_roles())
            else:
                await insufficient_perms(ctx)

        # No type specified/generic list
        else:
            await ctx.send(embed = players.Player_Manager.list_players())

    # Generic list
    else:
        await ctx.send(embed = players.Player_Manager.list_players())
# TODO - while game is in progress, roles are DM'd instead of sent in chat

# ---------------------------------------------------------------------------------------

# Start game
@client.command(pass_context = True)
async def start(ctx):
    await asyncio.sleep(0.1)

    # Can't start if waiting for confirmation
    global confirm_message, confirm_user
    if not confirm_message["start"] == None:
        embed = discord.Embed(color = 0xff0000, title = "Awaiting Confirmation", description = "Already waiting on confirmation for game start.")
        await ctx.send(embed = embed)
        return
    # TODO - Can't start if game is in progress
    if gameplay.game_phase > Game_Phase.Null:
        embed = discord.Embed(color = 0xff0000, title = "Game in Progress", description = "The game is already in progress!")
        await ctx.send(embed = embed)
        return

    # Check permission
    if check_perms(ctx):
        number_of_players = len(players.Player_Manager.players)
        global bypass_player_limit

        # Valid number of players
        if number_of_players >= Settings.get_min_player_count():
            embed = discord.Embed(color = 0x00ff00, title = "Start Game", description = "The following {} players are in the game:\n\n{}\nStart the game?".format(number_of_players, players.Player_Manager.list_players_raw(mention = True)))
            await confirmations.confirm_game_start(ctx, embed)

        # Confirm if player limit should be ignored
        elif bypass_player_limit and number_of_players > 0:
            embed = discord.Embed(color = 0xffff00, title = "Not Enough Players", description = "There are only {} out of the standard minimum of 12 players in the game:\n\n{}\nThe game may not function properly. Are you sure you want to begin?".format(number_of_players, players.Player_Manager.list_players_raw(mention = True)))
            await confirmations.confirm_game_start(ctx, embed)

        # No players
        elif number_of_players == 0:
            embed = discord.Embed(color = 0xff0000, title = "Not Enough Players", description = "No players are currently in the game.")
            await ctx.send(embed = embed)

        # Not enough players
        else:
            embed = discord.Embed(color = 0xff0000, title = "Not Enough Players", description = "There are only {} out of the minimum of {} players required for the game:\n\n{}".format(number_of_players, players.Player_Manager.list_players_raw(mention = True), Settings.get_min_player_count()))
            await ctx.send(embed = embed)
    
    # Insufficient permission
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

# TODO - lynching

# ---------------------------------------------------------------------------------------

# TODO - kill players & yeet command

@client.command(pass_context = True, aliases = ["yeet"])
async def kill(ctx, *args):
    await asyncio.sleep(0.1)

    # Check if game is running or not
    # if not misc.game_in_progress(gameplay.game_phase):
    #     description = "Cannot kill players if the game is not in progress."
    #     embed = discord.Embed(color = 0xff0000, title = "Cannot Kill Player", description = description)
    #     await ctx.send(embed = embed)
    #     return

    # Check permission
    if check_perms(ctx):
        #players.Player_Manager.kill_player()
        
        for i, user in enumerate(ctx.message.mentions):
            if i == 0:
                # Successfull kill
                if await players.Player_Manager.kill_player(user.id):

                    # TODO - send proper death message
                    await ctx.send("Killed {}".format(user.mention))

                # Could not kill
                else:
                    description = "Failed to kill {}, as they are not alive in the game.".format(user.mention)
                    embed = discord.Embed(color = 0xff0000, title = "Failed to Kill Player", description = description)
                    await ctx.send(embed = embed)

                return

    # Insufficient permission
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

# TODO - end game

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True, aliases = ["reset"])
async def resetgame(ctx):
    await asyncio.sleep(0.1)

    # Check permission
    if check_perms(ctx):
        # Send confirmation message
        embed = discord.Embed(color = 0xffff00, title = "⚠️ Reset Game? ⚠️", description = "Are you sure you want to reset the game?\nThis will remove all players and forcefully end the game if it is in progress.")
        message = await ctx.send(embed = embed)

        await confirmations.confirm_reset_game(ctx, message)

    # Insufficient permission
    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True, aliases = ["end"])
async def endgame(ctx):
    await asyncio.sleep(0.1)

    # Check permission
    if check_perms(ctx):
        # Cannot end game currently
        if not misc.game_in_progress(gameplay.game_phase):
            embed = discord.Embed(color = 0xff0000, title = "Failed to End Game", description = "The game is not in progress or is currently starting, and cannot be forcefully ended.")
            await ctx.send(embed = embed)
            return

        # Send confirmation message
        embed = discord.Embed(color = 0xffff00, title = "⚠️ Forcefully End Game? ⚠️", description = "Are you sure you want to forcefully end the game?")
        message = await ctx.send(embed = embed)

        await confirmations.confirm_end_game(ctx, message)

    # Insufficient permission
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True, aliases = ["skip"])
async def next(ctx):
    await asyncio.sleep(0.1)

    # Check permission
    if check_perms(ctx):
        # Skip Starting phase
        if gameplay.game_phase == Game_Phase.Starting and not gameplay.end_setup:
            await ctx.send("Skipping pre-game timer...")
            await asyncio.sleep(1)
            gameplay.end_setup = True

        # Skip Day, Evening, or Night phase
        elif gameplay.game_phase >= 3 and gameplay.game_phase <= 5:
            await ctx.send("Skipping phase...")
            gameplay.next_phase = True

        # Cannot skip
        else:
            embed = discord.Embed(color = 0xff0000, title = "Cannot Skip", description = "Cannot skip the current phase, or the game is not in progress.")
            await ctx.send(embed = embed)

    # Insufficient permission
    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True)
async def pause(ctx):
    await asyncio.sleep(0.1)

    # Game not in progress
    if gameplay.game_phase < Game_Phase.Morning or gameplay.game_phase > Game_Phase.Night:
        embed = discord.Embed(color = 0xff0000, title = "Game Not In Progress", description = "The game is not in progress, and cannot be paused.")
        await ctx.send(embed = embed)

    # Check permission
    elif check_perms(ctx):
        # Game is paused -> unpause
        if gameplay.pause_timer:
            gameplay.pause_timer = False
            embed = discord.Embed(color = 0x0080ff, title = "Game Unpaused", description = "The game has been unpaused.")
            await ctx.send(embed = embed)

        # Game is not paused -> pause
        else:
            gameplay.pause_timer = True
            embed = discord.Embed(color = 0xffff00, title = "⚠️ Game Paused ⚠️", description = "The game has been paused.")
            await ctx.send(embed = embed)

    # Insufficient permission
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True, aliases = ["timeremaining"])
async def time(ctx):
    await asyncio.sleep(0.1)

    # Day, Evening, or Night
    if gameplay.game_phase >= Game_Phase.Day and gameplay.game_phase <= Game_Phase.Night:
        # Warning if game is paused
        description = ""
        if gameplay.pause_timer:
            description += "⚠️ The game is currently paused. ⚠️\n\n"

        # Get time remaining string
        minutes_passed = (int)(gameplay.second_count / 60)
        minutes_remaining = (int)(gameplay.timer / 60)

        title = "{} of Day {}".format("Daytime" if gameplay.game_phase == 3 else gameplay.game_phase.name, gameplay.day_number)
        description += "{} minute{} {} passed.\n{} minute{} remain{}.".format("Less than 1" if minutes_passed < 1 else minutes_passed, \
            "" if minutes_passed <= 1 else "s", \
            "has" if minutes_passed <= 1 else "have", \
            \
            "Less than 1" if minutes_remaining < 1 else minutes_remaining, \
            "" if minutes_remaining <= 1 else "s", \
            "s" if minutes_remaining <= 1 else "")

        # Send embed / Yellow if paused, blue otherwise
        embed = discord.Embed(color = 0xffff00 if gameplay.pause_timer else 0x0080ff, title = title, description = description)
        await ctx.send(embed = embed)

    # Morning
    elif gameplay.game_phase == Game_Phase.Morning:
        title = "Morning of Day {}".format(gameplay.day_number)
        embed = discord.Embed(color = 0x0080ff, title = title, description = "")
        await ctx.send(embed = embed)

    # Game not in progress
    else:
        description = "The game is not in progress, so the time remaining cannot be checked."
        embed = discord.Embed(color = 0xff0000, title = "Game Not In Progress", description = description)
        await ctx.send(embed = embed)

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def spectate(ctx):
    await asyncio.sleep(0.1)

    # Check game in progress - Day, Evening, or Night
    if gameplay.game_phase >= 3 and gameplay.game_phase <= 5:
        # Check if active player
        if players.Player_Manager.has_player_id(ctx.author.id, dead_players = False) or players.Player_Manager.has_player_id(ctx.author.id, dead_players = True):
            embed = discord.Embed(color = 0xff0000, title = "Cannot Spectate", description = "Participating players cannot spectate the game.")
            await ctx.send(embed = embed)

        # Successfully spectate
        try:
            # Set permissions
            await channels["meeting"].set_permissions(ctx.author, read_messages = True, send_messages = False)
            await channels["voice_meeting"].set_permissions(ctx.author, view_channel = True, connect = True, speak = False)

            # Change nickname
            try:
                await ctx.author.edit(nick = "見 {}".format(ctx.author.display_name))
            except:
                embed = discord.Embed(color = 0xff0000, title = "Cannot Spectate", description = "Spectating permissions set up, but failed to change user's nickname.")

        # Error occured
        except Exception as e:
            embed = discord.Embed(color = 0xff0000, title = "Cannot Spectate", description = "An error occured while trying to spectate:\n{}".format(e))

    else:
        embed = discord.Embed(color = 0xff0000, title = "Cannot Spectate", description = "Cannot spectate the game if it is not in progress.")
        await ctx.send(embed = embed)

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def poll(ctx):
    await asyncio.sleep(0.1)

    text = ctx.message.content.replace("$poll", "").strip()
    embed = discord.Embed(title = "Poll by {}".format(ctx.message.author.display_name), description = text)
    embed.set_thumbnail(url = ctx.message.author.avatar_url)
    await ctx.message.delete()
    message = await ctx.send(embed = embed)

    await message.add_reaction('👍')
    await message.add_reaction('👎')
    await message.add_reaction('🤷')

@client.command(pass_context = True)
async def timer(ctx, *args):
    await asyncio.sleep(0.1)

    if check_perms(ctx):
        try:
            if float(args[0]) > 0:
                await ctx.send("**Starting a timer for {} minutes for {}...**".format(args[0], ctx.author.display_name))
                await asyncio.sleep(float(args[0]) * 60)
                await ctx.send("**TIMER FOR {} MINUTES BY {} HAS ENDED.**".format(args[0], ctx.author.mention))

            else:
                raise Exception("Invalid argument.")

        except:
            embed = discord.Embed(color = 0xff0000, title = "Invalid Arguments", description = "Please enter a valid number!")
            await ctx.send(embed = embed)

    else:
        await insufficient_perms(ctx)

@client.command(pass_context = True)
async def clearchat(ctx, *args):
    await asyncio.sleep(0.1)

    # Check permissions
    if check_perms(ctx, Perm_Level.Admin):
        # Get amount
        amount = 100
        try:
            amount = int(args[0])
        except:
            None

        # Send confirmation message
        message = await ctx.send("Clear {} message{} from chat?".format(amount, "" if amount == 1 else "s"))
        await confirmations.confirm_clear_chat(ctx, message, amount + 2)

    # Insufficient permissions
    else:
        await insufficient_perms(ctx)

# ---------------------------------------------------------------------------------------

@client.event
async def on_reaction_add(reaction, user):
    # Do nothing if the message was from the bot
    if user.bot:
        return

    channel = reaction.message.channel
    global confirm_message, confirm_user

    # ----------

    # Stop dead players from reacting
    try:
        # Check if game in progress, user is dead, and if message is in meeting channel
        if misc.game_in_progress(gameplay.game_phase) and not players.Player_Manager.has_player_id(user.id) and reaction.message.channel.id == channels["meeting"].id:
            await reaction.remove(user)

    except:
        None
        #await reaction.message.channel.send("Error: {}".format(e))

    # ----------

    # Start confirmation
    if confirm_message["start"] != None and reaction.message.id == confirm_message["start"].id and confirm_user["start"] == user:
        if reaction.emoji == '✅':
            confirm_message["start"] = None
            await gameplay.on_start(user, reaction.message.channel)

        elif reaction.emoji == '❌':
            confirm_message["start"] = None
            embed = discord.Embed(color = 0xff0000, title = "Game Start Cancelled", description = "Game start has been cancelled.")
            await channel.send(embed = embed)
        return

    # Role distribution confirmation
    if confirm_message["roles"] != None and reaction.message.id == confirm_message["roles"].id and confirm_user["roles"] == user:
        if reaction.emoji == '✅':
            confirm_message["roles"] = None
            await gameplay.continue_start(reaction.message.channel)

        elif reaction.emoji == '❌':
            confirm_message["roles"] = None
            await gameplay.on_reset()
            embed = discord.Embed(color = 0xff0000, title = "Game Start Cancelled", description = "Game start has been cancelled.")
            await channel.send(embed = embed)
        return

    # Clear chat confirmation
    if confirm_message["clear_chat"] != None and reaction.message.id == confirm_message["clear_chat"].id and confirm_user["clear_chat"] == user:
        if reaction.emoji == '✅':
            confirm_message["clear_chat"] = True

        elif reaction.emoji == '❌':
            confirm_message["clear_chat"] = None
            await channel.send("Clear chat cancelled.")
        return

    # End game confirmation
    if confirm_message["end_game"] != None and reaction.message.id == confirm_message["end_game"].id and confirm_user["end_game"] == user:
        if reaction.emoji == '✅':
            confirm_message["end_game"] = None

            gameplay.run_game = False
            await gameplay.reset_game(reaction.message.channel, clear_player_list = False)

        elif reaction.emoji == '❌':
            confirm_message["end_game"] = None
            await channel.send("Force ending of game cancelled.")
        return

    # Reset game confirmation
    if confirm_message["reset_game"] != None and reaction.message.id == confirm_message["reset_game"].id and confirm_user["reset_game"] == user:
        if reaction.emoji == '✅':
            confirm_message["reset_game"] = None

            gameplay.run_game = False
            await gameplay.reset_game(reaction.message.channel, clear_player_list = True)

        elif reaction.emoji == '❌':
            confirm_message["reset_game"] = None
            await channel.send("Reset game cancelled.")
        return

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def test(ctx):
    await asyncio.sleep(0.1)

    try:
        await ctx.author.edit(nick = "死 {}".format(ctx.author.display_name))

    except Exception as e:
        await ctx.send("Error: {}".format(e))

# ---------------------------------------------------------------------------------------

client.run(TOKEN)