from enum import Enum

class Animations(Enum):
    IDLE_A = 0
    IDLE_B = 1
    RUN = 2
    AIR_UP = 3
    AIR_DOWN = 4
    FRONT = 5
    BACK = 6
    WALL_SLIDE = 7
    SLIDE = 8

class States(Enum):
    GHOST = -1
    IDLE = 0
    RUN = 1
    JUMP = 2
    AIR = 3
    SLIDE = 4
    WALL_SLIDE = 5
    WALL_JUMP = 6
    HURT = 7
    DEAD = 8
