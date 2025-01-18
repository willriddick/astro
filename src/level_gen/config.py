from json import load, JSONDecodeError
from random import randint
from src.util import Direction

KEYS = ['rows', 'cols', 'main_length', 'room_count', 'bridge_count', 'item_count']
RANGES = ['branch_length_range']
WEIGHTS = ['weights', 'branch_weights']

class Config:
    """
    Configuration class that loads, validates, and stores the configuration data for the level generation.
    """
    def __init__(self, path: str):
        self.rows = None
        self.cols = None
        self.room_count = None
        self.main_length = None
        self.bridge_count = None
        self.item_count = None
        self.branch_length_range: tuple[int, int] = None
        self.weights: dict[Direction, int] = None
        self.branch_weights: dict[Direction, int] = None

        self._load_config(path)

    def _load_config(self, path: str) -> None:
        """Loads and validates the configuration file, updating the class fields."""
        try:
            with open(path, 'r') as file:
                config = load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {path}")
        except JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file: {path}")

        # Validate required keys and convert to tuples where necessary
        self._update(config)

    def _update(self, config: dict) -> None:
        """Validates required keys and sets values for the configuration with random selection from provided ranges."""
        # Validate and set main config keys (e.g., rows, cols)
        for key in KEYS:
            if key not in config:
                raise ValueError(f"Missing required attribute: '{key}' in configuration.")
            value = config[key]

            if isinstance(value, list) and len(value) == 2 and all(isinstance(i, int) for i in value):
                setattr(self, key, randint(value[0], value[1]))
            elif isinstance(value, int):
                setattr(self, key, value)  
            else:
                raise ValueError(f"Attribute '{key}' must be an int or list of 1 or 2 integers.")
        
        for key in RANGES:
            if key not in config:
                raise ValueError(f"Missing required attribute: '{key}' in configuration.")
            value = config[key]

            if isinstance(value, list) and len(value) == 2 and all(isinstance(i, int) for i in value):
                setattr(self, key, value)
            else:
                raise ValueError(f"Attribute '{key}' must be a list of 2 integers.")

        # Validate and set weights and branch_weights
        for key in WEIGHTS:
            if key not in config:
                raise ValueError(f"Missing required attribute: '{key}' in configuration.")
            value = config[key]

            if not isinstance(value, dict):
                raise ValueError(f"Attribute '{key}' must be a dictionary.")
            
            weights = {}
            for direction in Direction.cardinals():
                if direction.name not in value:
                    raise ValueError(f"Missing '{direction}' key in '{key}' dictionary.")
                if not isinstance(value[direction.name], int):
                    raise ValueError(f"Value for '{direction}' in '{key}' must be an integer.")
                weights[direction] = value[direction.name]

            setattr(self, key, weights)

    def __str__(self) -> str:
        def print_weights(self, weights: dict[Direction, int]) -> str:
            return ' '.join(f'{direction}:{weight}' for direction, weight in weights.items()) + '\n'

        return (f'Rows: {self.rows}\n'
                f'Columns: {self.cols}\n'
                f'Room Count: {self.room_count}\n'
                f'Main Path Length: {self.main_length}\n'
                f'Bridge Count: {self.bridge_count}\n'
                f'Item Count: {self.item_count}\n'
                f'Branch Length Range: {self.branch_length_range}\n'
                f'Weights: {print_weights(self.weights)}'
                f'Branch Weights: {print_weights(self.branch_weights)}')
