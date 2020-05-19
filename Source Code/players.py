import discord

# Stores information about each plater
class Player(object):
    def __init__(self, player_type):
        type = player_type

    @classmethod
    def is_human(cls):
        if type <= 5:
            return True
        return False

# Object that stores human
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
        cls.players.append(player)
        return "test"

    @classmethod
    def list_players(cls):
        text = ""
        for player in cls.players:
            text += "{}\n".format(player)
        return text