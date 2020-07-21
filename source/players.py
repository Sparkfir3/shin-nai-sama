import discord

import sys

sys.path.append("")
from settings import Settings

sys.path.append('source/data')
from enums import Player_Types
from dictionaries import channels

import random
from random import shuffle

# Stores information about each plater
class Player(object):
    def __init__(self, user_data, player_type):
        self._user = user_data
        self._type = player_type
        self._death_message = None

    # -------------------------------------------

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
    def display_name(self):
        return self.user.display_name

    @property
    def type(self):
        return self._type

    @property
    def death_message(self):
        return self._death_message

    @property
    def is_dead(self):
        return self._death_message == None

    # -------------------------------------------

    # Setters
    @type.setter
    def type(self, new_type):
        self._type = new_type

    @type.setter
    def death(self, new_string):
        self._type = new_string

    # -------------------------------------------
    
    # Other
    def is_human(self):
        return type <= Player_Types.Badger

    def on_wolf_side(self):
        return type >= Player_Types.Badger

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
    moderator = None

    players = []
    players_dead = []

    # Humans
    humans_all = []
    humans = []

    snake = None
    spider = None

    monkeys_all = []
    monkeys = []

    crow = None
    badger = None

    # Wolves
    wolves_all = []
    wolves = []

    # Attributes
    @classmethod
    def snake_alive(cls):
        return cls.snake != None

    @classmethod
    def spider_alive(cls):
        return cls.spider != None

    @classmethod
    def crow_alive(cls):
        return cls.crow != None

    @classmethod
    def badger_alive(cls):
        return cls.badger != None

    # -------------------------------------------

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

    @classmethod
    def has_player_id(cls, user_id, dead_players = False):
        # Alive players
        if not dead_players:
            for player in cls.players:
                if user_id == player.id:
                    return True
            return False

        # Dead players
        else:
            for player in cls.players_dead:
                if user_id == player.id:
                    return True
            return False

    # -----

    @classmethod
    async def kill_player(cls, user_id):
        # Check player alive
        for player in cls.players:
            try:
                # Kill player
                if player.id == user_id:
                    cls.players.remove(player)
                    cls.players_dead.append(player)

                    # Check snake
                    if cls.snake_alive() and cls.snake.id == user_id:
                        cls.snake = None
                        await channels["snake"].set_permissions(player.user, read_messages = True, send_messages = False)
                    # Check spider
                    if cls.spider_alive() and cls.spider.id == user_id:
                        cls.spider = None
                        await channels["spider"].set_permissions(player.user, read_messages = True, send_messages = False)
                    # Check crow
                    if cls.crow_alive() and cls.crow.id == user_id:
                        cls.crow = None
                    # Check badger
                    if cls.badger_alive() and cls.badger.id == user_id:
                        cls.badger = None

                    # Check monkey
                    for monkey in cls.monkeys:
                        if monkey.id == user_id:
                            cls.monkeys.remove(monkey)

                    # Check wolves
                    for wolf in cls.wolves:
                        if wolf.id == user_id:
                            cls.wolves.remove(wolf)
                            await channels["wolves"].set_permissions(wolf.user, read_messages = True, send_messages = False)
                            await channels["voice_wolves"].set_permissions(wolf.user, view_channel = True, connect = False, speak = False)
                            break

                    # Set channel permissions
                    await channels["meeting"].set_permissions(player.user, read_messages = True, send_messages = False)
                    try:
                        await channels["voice_meeting"].set_permissions(player.user, view_channel = True, connect = True, speak = False)
                        await player.user.edit(mute = True)
                    except:
                        None

                    await channels["dead"].set_permissions(player.user, read_messages = True, send_messages = True)

                    # Change nickname
                    try:
                        await player.user.edit(nick = "死 {}".format(player.user.display_name))

                    except:
                        await channels["moderator"].send("Failed to change the nickname of {} on death.".format(player.user.display_name))

                    # Return
                    return True

            # Error
            except Exception as e:
                print("Error killing player (channels not set up): {}".format(e))
                return False

        return False

    # -------------------------------------------

    # Listing players
    @classmethod
    def list_players(cls):
        # No players
        if len(cls.players) == 0 and len(cls.players_dead) == 0:
            return discord.Embed(color = 0x0080ff, title = "List of Players", description = cls.list_players_raw())

        # List players - dead vs. alive
        if len(cls.players_dead) > 0:
            # Alive
            description = "{} player{} alive:\n\n{}".format(len(cls.players), \
                "s are" if len(cls.players) != 1 else " is", \
                cls.list_players_raw(mention = True))
            embed = discord.Embed(color = 0x00080ff, title = "List of Players", description = description)

            # Dead
            description = "{} player{} dead:\n\n{}".format(len(cls.players_dead), \
                "s are" if len(cls.players_dead) != 1 else " is", \
                cls.list_players_raw(mention = True, dead_players = True))
            embed.add_field(name = "Dead Players", value = description, inline = False)

            return embed

        # List players - only alive
        description = "There {} {} player{} in the game:\n\n{}".format("is" if len(cls.players) == 1 else "are", \
            len(cls.players), \
            "s" if len(cls.players) != 1 else "", \
            cls.list_players_raw(mention = True))
        return discord.Embed(color = 0x0080ff, title = "List of Players", description = description)

    @classmethod
    def list_players_with_roles(cls):
        return discord.Embed(color = 0x0080ff, title = "List of Players", description = cls.list_players_raw(mention = True, role = True))

    @classmethod
    def list_players_raw(cls, mention = False, role = False, dead_players = False):
        text = ""
        # No players
        if len(cls.players) == 0:
            text = "No players are currently in the game."
        # Get players
        else:
            # Alive
            if not dead_players:
                for player in cls.players:
                    text += "{}{}\n".format(player.name if (not mention) else "<@{}>".format(player.id) \
                        , " - {}".format(player.role_to_string()) if role else "")

            # Dead
            else:
                for player in cls.players_dead:
                    text += "{}{}\n".format(player.name if (not mention) else "<@{}>".format(player.id) \
                        , " - {}".format(player.role_to_string()) if role else "")
        return text

    # -------------------------------------------

    # Start game
    @classmethod
    def distribute_roles(cls):
        wolf_count = cls.get_wolf_count()
        have_badger = random.randint(1, 100) < Settings.badger_chance

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

            players[-1].type = Player_Types.Spider
            cls.spider = players.pop()

            players[-1].type = Player_Types.Crow
            cls.crow = players.pop()

            if Settings.monkeys_enabled:
                for i in range(2):
                    players[-1].type = Player_Types.Monkey
                    cls.monkeys_all.append(players[-1])
                    cls.monkeys.append(players.pop())

            # Badger
            if have_badger:
                players[-1].type = Player_Types.Badger
                cls.badger = players.pop()

            # Regular humans
            for i in range(len(players)):
                players[-1].type = Player_Types.Human
                cls.humans_all.append(players[-1])
                cls.humans.append(players.pop())

        except:
            print("Error - not enough players to fully distribute roles.")
            return False
        return True

    @classmethod
    def get_wolf_count(cls):
        return max(1, int(len(cls.players) / 4)) if Settings.wolf_count == 0 else Settings.wolf_count

    # -------------------------------------------

    # Other
    @classmethod
    def reset(cls):
        cls.moderator = None

        for player in cls.players_dead:
            cls.players.append(player)
        cls.players_dead = []

        # Humans
        cls.humans_all = []
        cls.humans = []

        cls.snake = None
        cls.spider = None

        cls.monkeys_all = []
        cls.monkeys = []

        cls.crow = None
        cls.badger = None

        # Wolves
        cls.wolves_all = []
        cls.wolves = []