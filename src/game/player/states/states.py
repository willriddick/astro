from enum import Enum

class States(Enum):
    IDLE = 0
    RUN = 1
    JUMP = 2
    AIR = 3
    WALL_SLIDE = 4
    WALL_JUMP = 5
