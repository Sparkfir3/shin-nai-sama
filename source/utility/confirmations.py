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