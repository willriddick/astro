from typing import NamedTuple
from enum import Enum

# A immutable 2D vector (use when pygame.Vector2 is overkill)
class Vec2(NamedTuple):
    x: int
    y: int

class Direction(Enum):
    NONE = Vec2(0, 0)
    UP = Vec2(0, -1)
    RIGHT = Vec2(1, 0)
    DOWN = Vec2(0, 1)
    LEFT = Vec2(-1, 0)
    UP_LEFT = Vec2(-1, -1)
    UP_RIGHT = Vec2(1, -1)
    DOWN_RIGHT = Vec2(1, 1)
    DOWN_LEFT = Vec2(-1, 1)
