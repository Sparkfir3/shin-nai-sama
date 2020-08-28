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
    crow_enabled = True

    inu_enabled = False
    fox_enabled = False

    @classmethod
    def get_settings_embed(cls):
        description = """Wolf Count: {}
            Chance of Badger: {}%
            Monkeys Enabled: {}
            Crow Enabled: {}

            Shiba Inu Enabled: {}
            Fox Enabled: {}
            
            Minimum Player Count: {}""".format( \
            \
            "Auto" if cls.wolf_count == 0 else cls.wolf_count, \
            cls.badger_chance, \
            cls.monkeys_enabled, \
            cls.crow_enabled, \
            cls.inu_enabled, \
            cls.fox_enabled, \
            cls.get_min_player_count())
        return discord.Embed(color = 0x555555, title = "Shin'nai-sama Settings", description = description)

    @classmethod
    def get_min_player_count(cls):
        min_count = 2 # Snake, Spider
        if cls.badger_chance > 0: # Badger
            min_count += 1
            if cls.inu_enabled: # Shiba Inu
                min_count += 1
        if cls.monkeys_enabled: # Monkeys
            min_count += 2
        if cls.crow_enabled: # Crow
            min_count += 1
        if cls.fox_enabled: # Fox
            min_count += 1

        if cls.wolf_count > 0: # Wolf - manual
            min_count += cls.wolf_count
        else: # Wolf - automatic
            min_count += 2 if min_count >= 7 else 1

        return min_count