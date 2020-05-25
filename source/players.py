import discord

import sys
sys.path.append('source/data')
from enums import Player_Types

import random
from random import shuffle

# Stores information about each plater
class Player(object):
    def __init__(self, user_data, player_type):
        self._user = user_data
        self._type = player_type
        self._death_message = "Alive"

    # Getters
    @property
    def user(self):
        return self._user

    @property
    def id(self):
        return self._user.id

    @property
    def name(self):
        return "{}#{}".format(self.user.name.replace("@", ""), self.user.discriminator)

    @property
    def type(self):
        return self._type

    @property
    def death_message(self):
        return self._death_message

    @property
    def is_dead(self):
        return self._death_message == "Alive"

    # Setters
    @type.setter
    def type(self, new_type):
        self._type = new_type

    @type.setter
    def death(self, new_string):
        self._type = new_string

    # Other
    def is_human(self):
        return type <= 5

    def on_wolf_side(self):
        return type >= 5

    def role_to_string(self):
        if self.type == Player_Types.Human:
            return "Human"
        elif self.type == Player_Types.Snake:
            return "Snake"
        elif self.type == Player_Types.Spider:
            return "Spider"
        elif self.type == Player_Types.Monkey:
            return "Monkey"
        elif self.type == Player_Types.Crow:
            return "Crow"
        elif self.type == Player_Types.Badger:
            return "Badger"
        elif self.type == Player_Types.Wolf:
            return "Wolf"
        
        else:
            return "Error"

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

    # Player management
    @classmethod
    def add_player(cls, player, allow_dupes = False):
        if not allow_dupes:
            for p in cls.players:
                if p.name == player.name:
                    return False

        cls.players.append(player)
        return True

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

    # -------------------------------------------

    # Listing players
    @classmethod
    def list_players(cls):
        return discord.Embed(color = 0x0080ff, title = "List of Players", description = cls.list_players_raw(mention = True))

    @classmethod
    def list_players_with_roles(cls):
        return discord.Embed(color = 0x0080ff, title = "List of Players", description = cls.list_players_raw(mention = True, role = True))

    @classmethod
    def list_players_raw(cls, mention = False, role = False):
        text = ""
        # No players
        if len(cls.players) == 0:
            text = "No players are currently in the game."
        # Get players
        else:
            for player in cls.players:
                text += "{}{}\n".format(player.name if (not mention) else "<@{}>".format(player.id) \
                    , " - {}".format(player.role_to_string()) if role else "")
        return text

    # -------------------------------------------

    # Start game
    @classmethod
    def distribute_roles(cls):
        count = len(cls.players)
        wolf_count = int(count / 4)

        # TODO - adjusting badger chance depending on wolf-human ratio
        have_badger = random.randint(1, 100) < 50

        players = []
        for player in cls.players:
            players.append(player)
        shuffle(players)
        
        try:
            # Wolves
            for i in range(wolf_count):
                players[-1].type = Player_Types.Wolf
                cls.wolves_all.append(players[-1])
                cls.wolves.append(players.pop())

            # Power roles
            players[-1].type = Player_Types.Snake
            cls.snake = players.pop()
            cls.snake_alive = True

            players[-1].type = Player_Types.Spider
            cls.spider = players.pop()
            cls.spider_alive = True

            players[-1].type = Player_Types.Crow
            cls.crow = players.pop()
            cls.crow_alive = True

            for i in range(2):
                players[-1].type = Player_Types.Monkey
                cls.monkeys_all.append(players[-1])
                cls.monkeys.append(players.pop())

            # Badger
            if have_badger:
                players[-1].type = Player_Types.Badger
                cls.badger = players.pop()
                cls.badger_alive = True

            # Regular humans
            for i in range(len(players)):
                players[-1].type = Player_Types.Human
                cls.humans_all.append(players[-1])
                cls.humans.append(players.pop())

        except:
            print("Error - not enough players to fully distribute roles.")
            return False
        return True