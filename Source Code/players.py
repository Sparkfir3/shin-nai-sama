import discord

import sys
sys.path.append('Source Code/enums')
import player_types

# Stores information about each plater
class Player(object):
    def __init__(self, player_id, player_type):
        self._playerId = player_id.id
        self._name = "{}#{}".format(player_id.name.replace("@", ""), player_id.discriminator)
        self._type = player_type

    # Getters
    @property
    def id(self):
        return self._playerId

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    # Setters
    @type.setter
    def type(self, new_type):
        self._type = new_type

    # Other
    def is_human(self):
        return type <= 5

    def on_wolf_side(self):
        return type >= 5

# Class that stores players
class Player_Manager(object):
    players = []

    # Humans
    humans_all = []
    humans = []

    snake = None
    snake_alive = False

    spider = None
    spider_alive = False

    monkeys_all = []
    monkeys = []

    crow = None
    crow_alive = False

    badger = None
    badger_alive = False

    # Wolves
    wolves_all = []
    wolves = []

    @classmethod
    def add_player(cls, player):
        for p in cls.players:
            if p.name == player.name:
                return False

        cls.players.append(player)
        return True

    @classmethod
    def list_players(cls):
        text = ""
        # No players
        if len(cls.players) == 0:
            text = "No players are currently in the game."
        # Get players
        else:
            for player in cls.players:
                text += "{}\n".format(player.name)
        return discord.Embed(color = 0x0080ff, title = "List of Players", description = text)

    @classmethod
    def remove_player(cls, mentions):
        if len(cls.players) == 0:
            return "There are no players in the game to remove."

        count = 0
        for user in cls.players:
            for user_mentioned in mentions:
                if user.id == user_mentioned.id:
                    cls.players.remove(user)
                    mentions.remove(user_mentioned)
                    count += 1
        return "{} players have been removed from the game. There are now {} players in the game".format(count, len(cls.players))


    @classmethod
    def clear_players(cls):
        if len(cls.players) == 0:
            return "There are no players in the game to remove."

        amount = len(cls.players)
        cls.players = []
        return "All {} players have been removed.".format(amount)