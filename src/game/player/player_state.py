from enum import Enum

class PlayerState(Enum):
    GHOST = -1
    IDLE = 0
    RUN = 1
    JUMP = 2
    AIR = 3
    SLIDE = 4
    WALL_SLIDE = 5
    WALL_JUMP = 6
