from .direction import Direction 
from .status import Status
from .position import Position
from .attribute import Attribute

class Room:
    """
    Represents a room in the level with a unique index, position, set of attributes, 
    and dicitonary for adjacent directions.
    Attributes:
        index (int): Unique identifier.
        position (Position): The position object.
        attributes (list[RoomAttribute]): Stores the rooms associated attributes.
        adjacents (dict[Direction, AdjacentStatus]): Dictionary of directions and associated status
        key (int): Bitmask value (0-15) representing presence of LINKED rooms: UP (8) | DOWN (4) | LEFT (2) | RIGHT (1):
            0:      1:      2:      3:      4:      5:      6:      7:
              .       .       .       .       .       .       .       .
            . R .   . R →   ← R .   ← R →   . R .   . R →   ← R .   ← R →
              .       .       .       .       ↓       ↓       ↓       ↓
            8:      9:     10:     11:     12:     13:     14:     15:
              ↑       ↑       ↑       ↑       ↑       ↑       ↑       ↑
            . R .   . R →   ← R .   ← R →   . R .   . R →   ← R .   ← R →
              .       .       .       .       ↓       ↓       ↓       ↓
    """
    def __init__(self, index: int, position: Position):
        self.index = index
        self.position = position
        self.attributes: list[Attribute] = list()
        self.adjacents: dict[Direction, Status] = dict()
        self.key = 0
    
    def __str__(self) -> str:
        return f'R{self.index}'

    def __repr__(self) -> str:
        return f'{self.index:02} | {self.print_adjacents():12} | {self.print_attributes()}'
    
    def print_attributes(self) -> str:
        return ' '.join(str(attribute) for attribute in self.attributes)

    def print_adjacents(self) -> str:
        return ' '.join(f'{direction}{status}' for direction, status in self.adjacents.items())
    
    def get_status(self, direction: Direction) -> Status | None:
        """Returns the Status of the provided direction."""
        assert direction in Direction, 'direction must be a valid Direction'
        return self.adjacents.get(direction)
  
    def set_status(self, direction: Direction, status: Status):
        """Update the status of the specified direction."""
        assert direction in Direction, 'direction must be a valid Direction'
        self.adjacents[direction] = status
    
    def get_statuses(self) -> list[Status]:
        """Returns all Adjacent directions."""
        return self.adjacents.values()
    
    def has_status(self, status: Status) -> bool:
        """Returns whether the provided status exists within adjacents."""
        return status in self.get_statuses()
    
    def get_status_count(self, status: Status) -> int:
        """Returns the count of a provided status within adjacents."""
        return self.get_statuses().count(status)

    def get_directions(self, status: Status) -> list[Direction]:
        """
        Returns a set of Directions with the provided Status.
        Args: 
            status (Status): The status to build the list based on.
        Returns:
            list[Adjacent]: The filtered rooms.
        """
        output = list()
        for direction, cur_status in self.adjacents.items():
            if cur_status == status:
                output.append(direction)
        return output
    
    def update_key(self):
        """Update the key based on LINKED directions."""
        key = 0
        for direction, status in self.adjacents.items():
            if status == Status.LINKED:
                key += direction.mask
        self.key = key

    def add_attribute(self, attribute: Attribute):
        """Adds an attribute to the room."""
        if attribute not in self.attributes:
            self.attributes.append(attribute)

    def remove_attribute(self, attribute: Attribute):
        """Removes an attribute from the room."""
        if attribute in self.attributes:
            self.attributes.remove(attribute) 
    
    def has_attribute(self, attribute: Attribute) -> bool:
        """Returns whether the provide attribute is present."""
        return attribute in self.attributes
    
    def has_attributes(self, attributes: list[Attribute]) -> bool:
        """Returns whether the provide any of the provide attribute are present."""
        for attribute in attributes:
            if self.has_attribute(attribute):
                return True
        return False
    
    @staticmethod
    def is_branchable(room: 'Room') -> bool:
        """
        Determine if the given room is eligible for the BRANCH attribute. Useful for filter function.
        Args:
            room (Room): The room object to check.
        Returns:
            bool: True if the room can branch, False otherwise.
        """
        # Ensure the room has an empty Adjacent
        if not room.has_status(Status.EMPTY):
            return False
        # Ensure the room does not have restricted attributes 
        if room.has_attributes({Attribute.EXIT, Attribute.BRANCH}):
            return False
        return True
     
    @staticmethod
    def is_bridgeable(room: 'Room') -> bool:
        """
        Determine if the given room is eligible for the BRIDGE attribute. Useful for filter function.
        Args:
            room (Room): The room object to check.
        Returns:
            bool: True if the room can branch, False otherwise.
        """
        # Ensure the room has an unlinked Direction
        if not room.has_status(Status.UNLINKED):
            return False
        # Ensure the room does not have restricted attributes 
        if room.has_attributes({Attribute.EXIT, Attribute.BRIDGE, Attribute.BRANCH}):
            return False
        return True
    
    @staticmethod
    def is_itemable(room: 'Room') -> bool:
        """Determine if the given room is eligible for the ITEM attribute. Useful for filter function."""
        return not room.has_attributes({Attribute.ENTRANCE, Attribute.EXIT})
    
    @staticmethod
    def connect(room1: 'Room', room2: 'Room', direction: Direction, status: Status):
        """
        Connects room1 to room2 in the provided direction with a status.
        Args:
            room1 (Room): Must be an instance of Room.
            room2 (Room | None): If no room is provided (None), the status for room1 will be updated only. 
            direction (Direction): The direction from room1 to room2. Must be a valid Direction.
            status (Status): The status to provide. Must be either LINKED or UNLINKED if room2 is provided.
        """
        assert isinstance(room1, Room), 'room1 must be instance of Room'
        room1.set_status(direction, status)
        if room2 is not None:
            assert isinstance(room2, Room), 'room2 must be instance of Room'
            assert status in (Status.LINKED, Status.UNLINKED), 'status must be LINKED or UNLINKED when room2 is provide'
            room2.set_status(direction.opposite, status)
    
    @staticmethod
    def update_adjacents(level, room: 'Room'):
        """
        Updates the status of all directions from the given room based on the level provided.
        Args:
            room (Room): The room whose directions are being updated.
            level (Level): The level object containing the layout of rooms and their positions.
        """
        from .level import Level
        assert isinstance(level, Level), 'level must be of type Level'

        for direction in Direction:
            adjacent_room = level.get_room_at(room.position, direction)

            if isinstance(adjacent_room, Room):
                if adjacent_room.get_status(direction.opposite) == Status.LINKED:
                    Room.connect(room, adjacent_room, direction, Status.LINKED)
                else:
                    Room.connect(room, adjacent_room, direction, Status.UNLINKED)
            elif adjacent_room is None:
                Room.connect(room, adjacent_room, direction, Status.EMPTY)
