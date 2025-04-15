from src.util import Direction, Vec2
from .config import Config
from .room import Room
from .path import Path


class LevelMap:
    """
    Represents a level consisting of a 2D map of rooms.
    Attributes:
        config (Config): The config instance used to generate this level.
        map (dict[pygame.Vector2, Room]): A dictionary representing the map of rooms.
        index (int): Stores a unique index for the next room generated.
    """
    def __init__(self, config: Config):
        self.config = config
        self.paths: list[Path] = []
        self.map: dict[Vec2, Room] = {}
        self.item_count = 0
        self.index = 0
    
    def __str__(self) -> str:
        def print_rooms() -> str:
            return ''.join(f'{repr(room)}\n' for room in self.map.values()) + '\n'
        
        def print_paths() -> str:
            return ''.join(f'{path}\n' for path in self.paths) + '\n'
   
        return f'Rooms: \n{print_rooms()}Paths: \n{print_paths()}'
  
    def get_rooms(self) -> list[Room]:
        """Returns a list of the rooms."""
        return list(self.map.values())

    def get_room_at(self, position: Vec2, direction = Direction.NONE) -> Room | None | bool:
        """
        Retrieves the room at a specific position, applying an optional offset. 
        Returns:
            - Room if a room exists at the position.
            - None if the position is valid but no room exists.
            - False if the position is out of bounds.
        Args:
            position (Vec2): The position of the room to check for.
            direction (Direction, optional): An optional direction offset to apply.
        """
        position = Vec2.translate(position, direction)

        # If the position is out of bounds, return False
        if not (0 <= position.x < self.config.cols and 0 <= position.y < self.config.rows):
            return False
        
        # Return room or None
        return self.map.get(position)
    