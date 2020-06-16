import discord
import reactions

import asyncio

import sys
sys.path.append('source/data')
from dictionaries import confirm_message
from dictionaries import confirm_user

sys.path.append('source')
from gameplay import on_reset

# Asks if the user wants to start the game
async def confirm_game_start(ctx, embed):
    global confirm_message, confirm_user
    local_confirm_message = await ctx.send(embed = embed)
    confirm_message["start"] = local_confirm_message
    confirm_user["start"] = ctx.message.author
    await reactions.add_confirm_reactions(local_confirm_message)
    # on_reaction_add event handles yes/no answer

    # Timeout if user has not reacted in time (10 seconds)
    await asyncio.sleep(10)
    if confirm_message["start"] != None and local_confirm_message.id == confirm_message["start"].id:
        confirm_message["start"] = None
        confirm_user["start"] = None
        embed = discord.Embed(color = 0xff0000, title = "Timeout - Game Start", description = "Game start has been cancelled due to timing out.")
        await ctx.send(embed = embed)

# Asks if the user wants to confirm the role selection
async def confirm_roles(channel, message, user):
    global confirm_message, confirm_user
    confirm_message["roles"] = message
    confirm_user["roles"] = user
    await reactions.add_confirm_reactions(message)
    # on_reaction_add event handles yes/no answer

    # Timeout if user has not reacted in time (60 seconds)
    await asyncio.sleep(60)
    if confirm_message["roles"] != None and message.id == confirm_message["roles"].id:
        confirm_message["roles"] = None
        confirm_user["roles"] = None
        await on_reset()

        embed = discord.Embed(color = 0xff0000, title = "Timeout - Start Confirmation", description = "Game start has been cancelled due to timing out.")
        await channel.send(embed = embed)

# Asks if the user wants to confirm chat clear
async def confirm_clear_chat(ctx, message, amount):
    global confirm_message, confirm_user
    confirm_message["clear_chat"] = message
    confirm_user["clear_chat"] = ctx.author
    await reactions.add_confirm_reactions(message)
    # on_reaction_add event handles yes/no answer

    # Loop timer to wait for confirmation (10 seconds)
    i = 0.0
    while i <= 10:
        await asyncio.sleep(0.5)
        i += 0.5

        # Clear chat if user confirmed
        if confirm_message["clear_chat"] == True:
            await ctx.channel.purge(limit = amount)

            confirm_message["clear_chat"] = None
            confirm_user["clear_chat"] = None
            return

    # Timeout if the user has not reacted in time (10 seconds)
    if confirm_message["clear_chat"] != None and message.id == confirm_message["clear_chat"].id:
        confirm_message["clear_chat"] = None
        confirm_user["clear_chat"] = None

        embed = discord.Embed(color = 0xff0000, title = "Timeout - Clear Chat Confirmation", description = "Clear chat cancelled due to timing out.")
        await ctx.send(embed = embed)

# Asks if the user wants to confirm ending the game
async def confirm_end_game(ctx, message):
    global confirm_message, confirm_user
    confirm_message["end_game"] = message
    confirm_user["end_game"] = ctx.author
    await reactions.add_confirm_reactions(message)

    # Timeout if user has not reacted in time (10 seconds)
    await asyncio.sleep(10)
    if confirm_message["end_game"] != None and message.id == confirm_message["end_game"].id:
        confirm_message["end_game"] = None
        confirm_user["end_game"] = None

        embed = discord.Embed(color = 0xff0000, title = "Timeout - End Game Confirmation", description = "Force end game has been cancelled due to timing out.")
        await ctx.send(embed = embed)

        
# Asks if the user wants to confirm reseting the game
async def confirm_reset_game(ctx, message):
    global confirm_message, confirm_user
    confirm_message["reset_game"] = message
    confirm_user["reset_game"] = ctx.author
    await reactions.add_confirm_reactions(message)

    # Timeout if user has not reacted in time (10 seconds)
    await asyncio.sleep(10)
    if confirm_message["reset_game"] != None and message.id == confirm_message["reset_game"].id:
        confirm_message["reset_game"] = None
        confirm_user["reset_game"] = None

        embed = discord.Embed(color = 0xff0000, title = "Timeout - Reset Game Confirmation", description = "Force reset game has been cancelled due to timing out.")
        await ctx.send(embed = embed)