from enum import IntEnum

class Game_Phase(IntEnum):
    Null = 0
    Starting = 1
    Morning = 2
    Day = 3
    Evening = 4
    Night = 5
    Ending = 6

class Perm_Level(IntEnum):
    Admin = 0
    Moderator = 1
    Player = 2

class Player_Types(IntEnum):
    Human = 0
    Snake = 1
    Spider = 2
    Monkey = 3
    Crow = 4
    Badger = 5
    Wolf = 6