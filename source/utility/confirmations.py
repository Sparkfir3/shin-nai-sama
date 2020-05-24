import discord
import reactions

import asyncio

import sys
sys.path.append('source/data')
from dictionaries import confirm_message
from dictionaries import confirm_user

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
