import discord

from dotenv import load_dotenv
load_dotenv()

import os

TOKEN = os.getenv("TOKEN")
DEVMODE = os.getenv("DEVMODE")

class Settings:
    badger_chance = 50
    monkeys_enabled = True

    @classmethod
    def get_settings_embed(cls):
        description = "Chance of Badger: {}%\n \
            Monkeys Enabled: {}".format(cls.badger_chance, cls.monkeys_enabled)
        return discord.Embed(color = 0x555555, title = "Shin'nai-sama Settings", description = description)

    @classmethod
    def get_min_player_count(cls):
        min = 4 # Snake, Spider, Crow, Wolf
        if cls.badger_chance > 0: # Badger
            min += 1
        if cls.monkeys_enabled: # Monkeys
            min += 2

        return min