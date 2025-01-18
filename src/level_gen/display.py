import numpy as np
from src.util import Direction
from .level_map import LevelMap
from .room import Room
from .status import Status

HORIZONTAL = '─'
VERTICAL = '│'
TOP_LEFT_CORNER = '╭'
TOP_RIGHT_CORNER = '╮'
BOTTOM_RIGHT_CORNER = '╯'
BOTTOM_LEFT_CORNER = '╰'

class Display:
    """
    A class that generates and displays an ASCII representation of a level map.
    Attributes:
        level (LevelMap): The level to display.
        room_rows (int): Number of rows for each room
        room_cols (int): Number of columns for each room
        rows (int): Number of rows in the level map.
        cols (int): Number of columns in the level map.
        room_size (int): Size of each room in the grid, in characters.
        display (list[list[str]]): 2D array representing the ASCII display of the map.
    """
    def __init__(self, level: LevelMap):
        self.level = level
        self.room_rows = 5
        self.room_cols = 10

        # Calculate rows/col of display 
        self.rows = level.config.rows * self.room_rows 
        self.cols = level.config.cols * self.room_cols 

        self.display = np.full((self.rows, self.cols), ' ', dtype=str)

        self.ROOM_TEMPLATE = Display._create_template(self.room_rows, self.room_cols)
        self.connection_map = {
            Direction.UP:    (0, self.room_cols // 2, '┴'), 
            Direction.DOWN:  (self.room_rows - 1, self.room_cols // 2, '┬'),  
            Direction.LEFT:  (self.room_rows // 2, 0, '┤'),
            Direction.RIGHT: (self.room_rows // 2, self.room_cols - 1, '├')
        }
    
    def __str__(self) -> str:
        self._update_display()
        # Flip the array vertically to correct for filling the array top to bottom
        return '\n'.join([''.join(row) for row in self.display if not self._is_empty_row(row)])
    
    def _is_empty_row(self, row: np.ndarray) -> bool:
        """Check if a row is empty (contains only spaces)."""
        return np.all(row == ' ')
    
    def _update_display(self):
        """Updates the display array by adding all rooms from the level map."""
        for room in (self.level.map.values()):
            self._add_room(room)
    
    def _add_room(self, room: Room):
        """
        Adds the ASCII representation of a single room to the display grid.
        Args:
            room (Room): The room to be added to the display.
        """
        origin_x = room.position.x * self.room_cols
        origin_y = room.position.y * self.room_rows
        room_display = self._get_room_display(room)

        for y_offset in range(self.room_rows):
            for x_offset in range(self.room_cols):
                self.display[origin_y + y_offset, origin_x + x_offset] = room_display[y_offset, x_offset]
    
    def _get_room_display(self, room: Room) -> np.ndarray:
        """
        Generates the ASCII representation of a room.
        Args:
            room (Room): The room for which the ASCII display is being generated.
        Returns:
            np.ndarray: A 2D array of characters representing the room and its connections.
        """
        assert room is not None, 'Room cannot be none'
        room_display = self.ROOM_TEMPLATE.copy()
        
        # Place room information
        attributes = ' '.join(f'{attr}' for attr in room.attributes)
        info_str = f'{room.index} {attributes}'.ljust(self.room_cols - 2)
        position_str = f'{room.position}'.ljust(self.room_cols - 2)
        room_display[1, 1:-1] = list(info_str)
        room_display[2, 1:-1] = list(position_str)

        # Add room connections based on adjacent status
        for direction, status in room.adjacents.items():
            if status == Status.LINKED:
                y, x, symbol = self.connection_map[direction]
                room_display[y, x] = symbol

        return room_display

    @staticmethod
    def _create_template(rows: int, cols: int) -> np.ndarray:
        """Creates a template room display with outline characters."""
        template = np.full((rows, cols), ' ', dtype=str)  
        template[0, 1:-1]  = HORIZONTAL
        template[-1, 1:-1] = HORIZONTAL
        template[1:-1, 0]  = VERTICAL
        template[1:-1, -1] = VERTICAL
        template[0, 0]     = TOP_LEFT_CORNER
        template[0, -1]    = TOP_RIGHT_CORNER
        template[-1, 0]    = BOTTOM_LEFT_CORNER
        template[-1, -1]   = BOTTOM_RIGHT_CORNER
        return template
