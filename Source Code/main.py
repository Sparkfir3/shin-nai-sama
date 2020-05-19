import discord
import players

from discord.ext import commands
from discord.utils import get
from enum import Enum

client = commands.Bot(command_prefix = '$')
client.remove_command("help")

@client.event
async def on_ready():
    print("We have loggined in as {0.user}".format(client))

class Player_Types(Enum):
    Human = 0
    Snake = 1
    Spider = 2
    Monkey = 3
    Crow = 4
    Badger = 5
    Wolf = 6

# ---------------------------------------------------------------------------------------

@client.group(pass_context = True)
async def help(ctx):
    if ctx.invoked_subcommand is None:
        description = "$help - Lists all available bot comamnds."
        description += "\n" + "$ping - Test command that gives the bot\'s latency time."
        
        embed = discord.Embed(color = 0x555555, title = "Shin'nai-sama Commands", description = description)
        await ctx.send(embed = embed)

@client.command(pass_context = True)
async def ping(ctx):
	await ctx.send("Pong! Latency: {} ms".format(round(client.latency, 1)))

# ---------------------------------------------------------------------------------------

# Player management
@client.command(pass_context = True, aliases = ["add"])
async def addplayer(ctx, *args):
    # Do nothing if no arguments
    if len(args) == 0:
        await ctx.send("Please enter a valid player!")
        return

    # Add player
    players.Player_Manager.add_player(args[0])
    await ctx.send("Added {} to list of players".format(args[0]))
    

@client.command(pass_context = True)
async def listplayers(ctx):
    message = players.Player_Manager.list_players()
    await ctx.send(message)

# ---------------------------------------------------------------------------------------

# TODO - start game

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

def check_valid_user(name):

    return False

# ---------------------------------------------------------------------------------------

def check_perms(ctx):
    id = discord.utils.get(ctx.guild.roles, name="Moderator")
    if id in ctx.author.roles:
        return True
    return False

def insufficient_perms():
	description = "The \"Moderator\" or \"Game Master\" role is required to use this command."
	embed = discord.Embed(color = 0xff0000, title = "Insufficient Permissions", description = description)
	return embed

# ---------------------------------------------------------------------------------------

@client.command(pass_context = True)
async def test(ctx):
    description = ctx.message.author.name
    await ctx.send(description)

# ---------------------------------------------------------------------------------------

# Access code removed for security purposes
client.run("NzEyMTM2NzY0NjAwNjE0OTMy.XsNLGw.DoJdDQLfd5BD44KfI7JSUZHOeKk")