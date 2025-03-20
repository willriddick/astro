from enum import Enum


class GameStates(Enum):
    MAIN_MENU = 0
    SINGLEPLAYER = 1
    LOBBY_HOST = 2
    LOBBY_JOIN = 3
    LOBBY = 4
    MULTIPLAYER = 5
