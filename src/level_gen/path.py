from .room import Room


class Path:
    """
    Represents a path consisting of rooms in a level.
    Attributes:
        index (int): Unique identifier for the path.
        start (Room): The starting room of the path.
        end (Room): The current end room of the path.
        target_length (int): The desired length of the path.
        length (int): The current length of the path.
        rooms (list[Room]): A list of rooms in the path.
        complete (bool): Indicates whether the path is complete.
    """
    def __init__(self, index: int, start_room: Room, target_length: int):
        self.index = index
        self.start: Room = start_room
        self.end: Room = start_room
        self.target_length: int = target_length
        self.length: int = 0
        self.rooms: list[Room] = [start_room]
        self.complete: bool = False
    
    def __str__(self) -> str:
        return f'P{self.index} | ' + ' '.join(str(room) for room in self.rooms) 
    
    def add_room(self, room: Room): 
        """Adds a room to this path."""
        self.rooms.append(room)
        self.end = room
        self.length += 1

    def remove_room(self, room: Room): 
        """Removes the provided room from this path."""
        self.rooms.remove(room)
        self.end = self.rooms[-1]
        self.length -= 1

    def get_room(self, index: int) -> Room:
        """Returns the room at the specified index within this path."""
        return self.rooms[index]
