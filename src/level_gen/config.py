from random import randint
from src.util import Direction

class Config:
    """
    Configuration class that loads, validates, and stores the configuration data for the level generation.
    """
    def __init__(self, 
            rows: tuple[int, int],
            cols: tuple[int, int],
            room_count: tuple[int, int],
            main_length: tuple[int, int],
            bridge_count: tuple[int, int],
            item_count: int,
            branch_length_range: tuple[int, int],
            weights: dict[Direction, int],
            branch_weights: dict[Direction, int]
        ):
        self.rows = randint(rows[0], rows[1])
        self.cols = randint(cols[0], cols[1])
        self.room_count = randint(room_count[0], room_count[1])
        self.main_length = randint(main_length[0], main_length[1])
        self.bridge_count = randint(bridge_count[0], bridge_count[1])
        self.item_count = item_count
        self.branch_length_range = branch_length_range
        self.weights = weights
        self.branch_weights = branch_weights
    
CONFIGS = [
    Config(
        rows=(3, 3),
        cols=(3, 3),
        main_length=(3, 4),
        room_count=(6, 8),
        bridge_count=(2, 3),
        item_count=3,
        branch_length_range=(1, 3),
        weights={
            Direction.UP: 10,
            Direction.DOWN: 0,
            Direction.LEFT: 5,
            Direction.RIGHT: 5,
        },
        branch_weights={
            Direction.UP: 5,
            Direction.DOWN: 5,
            Direction.LEFT: 5,
            Direction.RIGHT: 5,
        },
    ),

    Config(
        rows=(4, 5),
        cols=(3, 3),
        room_count=(7, 12),
        main_length=(4, 5),
        bridge_count=(3, 3),
        item_count=4,
        branch_length_range=(1, 3),
        weights={
            Direction.UP: 10,
            Direction.DOWN: 0,
            Direction.LEFT: 5,
            Direction.RIGHT: 5,
        },
        branch_weights={
            Direction.UP: 5,
            Direction.DOWN: 5,
            Direction.LEFT: 5,
            Direction.RIGHT: 5,
        },
    )
]