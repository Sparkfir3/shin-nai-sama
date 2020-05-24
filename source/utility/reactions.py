import discord

import sys
sys.path.append('source/data')
# import emoji dictionaries

async def add_confirm_reactions(message):
    await message.add_reaction('✅')
    await message.add_reaction('❌')
