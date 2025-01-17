from enum import Enum
from .vec2 import Vec2

class Direction(Enum):
    """
    Represents a direction in the map with a name, bitmask value, and movement vector.
    Attributes:
        vector (Vec2): A tuple representing the movement vector (dx, dy) for the direction.
        mask (int): A bitmask value representing the direction.
        symbol (str): A string symbol representing the direction.
    """
    NONE = (Vec2(0, 0), 0, ' ')
    RIGHT = (Vec2(1,  0), 1, '→')
    LEFT  = (Vec2(-1, 0), 2, '←')
    DOWN  = (Vec2(0,  1), 4, '↓')
    UP    = (Vec2(0, -1), 8, '↑')
    UP_LEFT = (Vec2(-1, -1), 16, '↖')
    UP_RIGHT = (Vec2(1, -1), 32, '↗')
    DOWN_RIGHT = (Vec2(1, 1), 64, '↘')
    DOWN_LEFT = (Vec2(-1, 1), 128, '↙')

    def __init__(self, vector: Vec2, mask: int, symbol: str):
        self.vector = vector
        self.mask = mask
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
    
    @classmethod
    def cardinals(cls) -> list['Direction']:
        """Returns the four cardinal directions."""
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]

    @classmethod
    def diagonals(cls) -> list['Direction']:
        """Returns the four cardinal directions."""
        return [cls.UP_LEFT, cls.UP_RIGHT, cls.DOWN_LEFT, cls.DOWN_RIGHT]
    
    @property
    def opposite(self) -> 'Direction':
        """Returns the opposite direction."""
        return {
            Direction.NONE: Direction.NONE,
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.DOWN: Direction.UP,
            Direction.UP: Direction.DOWN,
            Direction.DOWN_RIGHT: Direction.UP_LEFT,
            Direction.DOWN_LEFT: Direction.UP_RIGHT,
            Direction.UP_RIGHT: Direction.DOWN_LEFT,
            Direction.UP_LEFT: Direction.DOWN_RIGHT,
        }[self]

