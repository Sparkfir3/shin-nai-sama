import discord

import sys
sys.path.append('source/data')
from dictionaries import channels

async def get_dm_channel(user):
    channel = user.dm_channel
    if channel == None:
        channel = await user.create_dm()
    return channel

async def get_participant_role():
    guild = channels["meeting"].guild
    role = discord.utils.get(guild.roles, name="Feast Participant")

    # Create role
    if role == None:
        return await guild.create_role(name = "Feast Participant")

    # Delete role and create new one
    else:
        await role.delete()
        return await guild.create_role(name = "Feast Participant")

async def get_dead_role():
    guild = channels["meeting"].guild
    role = discord.utils.get(guild.roles, name="Dead")
    if role == None:
        return await guild.create_role(name = "Dead")
    else:
        return role

def ordinalize(number):
    mod10 = number % 10
    mod100 = number % 100
    
    if mod10 == 1 and mod100 != 11:
        return "{}st".format(number)
    elif mod10 == 2 and mod100 != 12:
        return "{}nd".format(number)
    elif mod10 == 3 and mod100 != 13:
        return "{}rd".format(number)
    else:
        return "{}th".format(number)