from random import seed, choice, randint
from typing import TypeVar
from src.util import Direction
from .config import Config
from .level import Level
from .room import Room
from .path import Path
from .status import Status
from .attribute import Attribute
from .position import Position

class LevelBuilder:
    @staticmethod
    def generate_level(config_path: str, _seed: int | float | str = None) -> Level:
        """
        Build a Level instance from a random seed and JSON configuration.
        """
        if _seed is not None:
            seed(_seed)
        
        # Create config and level
        config = Config(config_path)
        level = Level(config)
        
        # Set ENTRANCE
        start_position: Position = Position(randint(0, config.cols - 1), config.rows - 1)
        start_room = LevelBuilder._create_room(level, start_position)
        start_room.add_attribute(Attribute.ENTRANCE)

        # Generate main path
        LevelBuilder._create_path(level, start_room, config.main_length - 1, config.weights) # Subtract 1 because start_room was created already

        # Set EXIT
        end_room = level.paths[0].get_room(-1) # Gets the most recently generated room in path 0
        end_room.add_attribute(Attribute.EXIT)

        # Generate branches
        LevelBuilder._generate_branches(level, config)

        # Add links
        LevelBuilder._generate_bridges(level, config)

        # Add collectables
        LevelBuilder._generate_items(level, config)

        # Update keys
        for room in level.get_rooms():
            room.update_key()

        # Return generated level
        return level

    @staticmethod
    def _generate_branches(level: Level, config: Config) -> bool:
        # Get remainging count of rooms to generate
        count = config.room_count - level.index

        while count > 0:
            # Get length
            rand_length = randint(config.branch_length_range[0], config.branch_length_range[1])
            length = min(count, rand_length)

            # Get rooms that can branch
            rooms = list(filter(Room.is_branchable, level.get_rooms()))

            # If none exist, exit early 
            if not rooms:
                return False

            # Chose room to branch from
            room = choice(rooms)
            room.add_attribute(Attribute.BRANCH)

            # Generate a branch starting at room
            LevelBuilder._create_path(level, room, length, config.weights)

            count = config.room_count - level.index
        
        # Return true meaning 'count' rooms were generated
        return True

    @staticmethod
    def _generate_bridges(level: Level, config: Config) -> bool:
        for _ in range(config.bridge_count):
            rooms = list(filter(Room.is_bridgeable, level.get_rooms()))
            if not rooms:
                return False

            room1: Room = choice(rooms)
            room1.add_attribute(Attribute.BRIDGE)
            direction = choice(list(room1.get_directions(Status.UNLINKED)))
            room2: Room = level.get_room_at(room1.position, direction)
            Room.connect(room1, room2, direction, Status.LINKED)
        
        return True

    @staticmethod
    def _generate_items(level: Level, config: Config) -> bool:
        for _ in range(config.item_count):
            rooms = list(filter(Room.is_itemable, level.get_rooms()))
            if not rooms:
                return False
            
            room: Room = choice(rooms)
            room.add_attribute(Attribute.ITEM_ONE)
        
        return True
    
    @staticmethod
    def _create_path(level: Level, start_room: Room, length: int, weights: dict[Direction, int]) -> Path:
        """
        Create a path starting from the specified room and extending for a given length.
        Args:
            start_room (Room): The room where the path generation begins.
            length (int): The desired number of rooms in the path.
        Returns:
            bool: Whether the path was fully built 
        Raises:
            AssertionError: If an invalid position is chosen or no room can be created at the new position.
        """
        path = Path(len(level.paths), start_room, length)
        level.paths.append(path)

        room = start_room
        direction: Direction = None
        position = room.position

        for _ in range(length):
            # Get EMPTY directions from the current room
            available = room.get_directions(Status.EMPTY)
            if not available:
                return path

            # Get a new direction 
            direction = LevelBuilder._get_weighted_choice(available, weights)
            if direction is None:
                return path

            # Update position
            position = position.move(direction)

            # Store previous room and direction
            prev_room = room 
            prev_dir = direction

            # Create new room
            room = LevelBuilder._create_room(level, position)
            path.add_room(room)
            
            # If previous room exists, connect room and prev_room
            if prev_room:
                Room.connect(prev_room, room, prev_dir, Status.LINKED)
        
        path.complete = True
        return path
    
    @staticmethod
    def _create_room(level: Level, position: Position) -> Room:
        """
        Creates and returns a Room object at the specified position in the given level.
        Args:
            level (Level): The level in which to create the room.
            position (Position): The position to place the room.
        Returns:
            Room: The newly created Room object.
        Raises:
            AssertionError: If the position is already occupied by another room or is out of bounds.
        """
        prev_room = level.get_room_at(position)
        assert prev_room is not False, 'Position invalid'
        assert prev_room is None, 'Position not EMPTY'

        new_room = Room(level.index, position)
        level.index += 1
        level.map[position] = new_room
        Room.update_adjacents(level, new_room)  # Assuming this updates adjacents in the Level map
        return new_room


    T = TypeVar('T')
    @staticmethod
    def _get_weighted_choice(available: list[T], weights: dict[T, int]) -> T | None:
        """
        Selects an item from the available list based on weighted probabilities.
        
        Args:
            available (Sequence[T]): A sequence of available items.
            weights (Mapping[T, int]): A mapping of items to their associated weights.
            
        Returns:
            Optional[T]: A randomly selected item from the available items, 
            or None if no items are available with non-zero weights.
        """
        # Filter out items with weights of 0 or non-existent weights
        available = [item for item in available if weights.get(item, 0) > 0]

        if not available:
            return None

        # Calculate the total weight of the available items
        total_weight = sum(weights[item] for item in available)
        key = randint(0, total_weight - 1) if total_weight > 1 else 0

        # Select an item based on the random key and cumulative weights
        counter = 0
        for item in available:
            counter += weights[item]  # Use the weight from the weights dict
            if counter > key:
                return item

        return available[-1]  # Fallback in case no item is selected
