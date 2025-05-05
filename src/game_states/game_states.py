from enum import Enum


class GameStates(Enum):
    MAIN_MENU = 0
    LOBBY_SINGLEPLAYER = 1
    SINGLEPLAYER = 2
    LOBBY_HOST = 3
    LOBBY_JOIN = 4
    MULTIPLAYER = 5
