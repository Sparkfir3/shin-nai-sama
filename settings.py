import discord

from dotenv import load_dotenv
load_dotenv()

import os

TOKEN = os.getenv("TOKEN")
DEVMODE = os.getenv("DEVMODE")

class Settings:
    wolf_count = 0
    badger_chance = 100
    monkeys_enabled = True

    @classmethod
    def get_settings_embed(cls):
        description = "Wolf Count: {} \
            \nChance of Badger: {}% \
            \nMonkeys Enabled: {} \
            \n\nMinimum Player Count: {}".format( \
            \
            "Auto" if cls.wolf_count == 0 else cls.wolf_count, \
            cls.badger_chance, \
            cls.monkeys_enabled, \
            cls.get_min_player_count())
        return discord.Embed(color = 0x555555, title = "Shin'nai-sama Settings", description = description)

    @classmethod
    def get_min_player_count(cls):
        min = 3 + (1 if cls.wolf_count == 0 else cls.wolf_count) # Snake, Spider, Crow, Wolf
        if cls.badger_chance > 0: # Badger
            min += 1
        if cls.monkeys_enabled: # Monkeys
            min += 2

        return min