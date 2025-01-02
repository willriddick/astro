from enum import Enum

class Direction(Enum):
    """
    Represents a direction in the map with a name, bitmask value, and movement vector.
    Attributes:
        vector (Tuple[int, int]): A tuple representing the movement vector (dx, dy) for the direction.
        mask (int): A bitmask value representing the direction.
        symbol (str): A string symbol representing the direction.
    """
    UP    = ((0, -1), 8, '↑')
    DOWN  = ((0,  1), 4, '↓')
    LEFT  = ((-1, 0), 2, '←')
    RIGHT = ((1,  0), 1, '→')

    def __init__(self, vector: tuple[int, int], mask: int, symbol: str):
        self.vector = vector
        self.mask = mask
        self.symbol = symbol

    def __str__(self) -> str:
        return self.symbol
    
    @property
    def opposite(self) -> 'Direction':
        """Returns the opposite direction."""
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }[self]
