import discord

import sys
sys.path.append('source/data')
from enums import Perm_Level

sys.path.append('source')
import players

def check_perms(ctx, level = Perm_Level.Admin):
    # Admin level
    if level == Perm_Level.Admin or level == Perm_Level.Moderator: # Difference between Admin and Moderator is deprecated
        id1 = discord.utils.get(ctx.guild.roles, name="Gamemasters")
        id2 = discord.utils.get(ctx.guild.roles, name="Moderator")
        if id1 in ctx.author.roles or id2 in ctx.author.roles:
            return True
        return False

    # Player level
    elif level == Perm_Level.Player:
        if check_perms(ctx, Perm_Level.Moderator):
            return True

        for player in players.Player_Manager.players:
            if player.id == ctx.author.id:
                return True
        return False

    return False

async def insufficient_perms(ctx, level = Perm_Level.Admin):
    embed = None
    # Player
    if level == Perm_Level.Player:
        description = "You do not have permission to use this command right now.\nOnly active players may use this command."
        embed = discord.Embed(color = 0xff0000, title = "Insufficient Permissions", description = description)

    # Moderator or Admin
    else:
        description = "You do not have permission to use this command."
        embed = discord.Embed(color = 0xff0000, title = "Insufficient Permissions", description = description)

    await ctx.send(embed = embed)
