from typing import NamedTuple
from enum import Enum

class Vec2(NamedTuple):
    """
    A immutable 2D vector (use when pygame.Vector2 is overkill)
    """
    x: int
    y: int
