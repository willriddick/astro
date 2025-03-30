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
        self.rows = rows
        self.cols = cols
        self.room_count = room_count
        self.main_length = main_length
        self.bridge_count = bridge_count
        self.item_count = item_count
        self.branch_length_range = branch_length_range
        self.weights = weights
        self.branch_weights = branch_weights
    
CONFIGS = [
    Config(
        rows=3,
        cols=3,
        main_length=4,
        room_count=7,
        bridge_count=2,
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
        rows=5,
        cols=3,
        main_length=7,
        room_count=10,
        bridge_count=2,
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

]
