from random import seed, choice, randint
from src.util import Direction, Vec2, get_weighted_choice
from .config import Config
from .level_map import LevelMap
from .room import Room
from .path import Path
from .status import Status
from .attribute import Attribute

def generate_level(
        config_path: str, 
        _seed: int | float | str | bytes | bytearray | None = None
    ) -> LevelMap:
    """
    Build a Level instance from a random seed and JSON configuration.
    """
    if _seed is not None:
        seed(_seed)
    
    # Create config and level
    config = Config(config_path)
    level = LevelMap(config)
    
    # Set ENTRANCE
    start_position = Vec2(randint(0, config.cols - 1), config.rows - 1)
    start_room = _create_room(level, start_position)
    start_room.add_attribute(Attribute.ENTRANCE)

    # Generate main path
    _create_path(level, start_room, config.main_length - 1, config.weights) # Subtract 1 because start_room was created already

    # Set EXIT
    end_room = level.paths[0].get_room(-1) # Gets the most recently generated room in path 0
    end_room.add_attribute(Attribute.EXIT)

    # Generate branches
    _generate_branches(level, config)

    # Add links
    _generate_bridges(level, config)

    # Add collectables
    _generate_items(level, config)

    # Update keys
    for room in level.get_rooms():
        room.update_key()

    # Return generated level
    return level

def _generate_branches(level: LevelMap, config: Config) -> bool:
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
        _create_path(level, room, length, config.weights)

        count = config.room_count - level.index
    
    # Return true meaning 'count' rooms were generated
    return True

def _generate_bridges(level: LevelMap, config: Config) -> bool:
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

def _generate_items(level: LevelMap, config: Config) -> bool:
    for _ in range(config.item_count):
        rooms = list(filter(Room.is_itemable, level.get_rooms()))
        if not rooms:
            return False
        
        room: Room = choice(rooms)
        room.add_attribute(Attribute.ITEM_ONE)
    
    return True

def _create_path(level: LevelMap, start_room: Room, length: int, weights: dict[Direction, int]) -> Path:
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
        direction = get_weighted_choice(available, weights)
        if direction is None:
            return path

        # Update position
        position = Vec2.move(position, direction)

        # Store previous room and direction
        prev_room = room 
        prev_dir = direction

        # Create new room
        room = _create_room(level, position)
        path.add_room(room)
        
        # If previous room exists, connect room and prev_room
        if prev_room:
            Room.connect(prev_room, room, prev_dir, Status.LINKED)
    
    path.complete = True
    return path

def _create_room(level: LevelMap, position: Vec2) -> Room:
    """
    Creates and returns a Room object at the specified position in the given level.
    Args:
        level (Level): The level in which to create the room.
        position (Vec2): The position to place the room.
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
