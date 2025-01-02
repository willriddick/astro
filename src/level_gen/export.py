from json import dump
from .level import Level

@staticmethod
def export(level: Level, filename: str):
    """
    Exports the provided level data to a JSON file.
    Args:
        filename (str): The name of the file to save the level data to.
    """
    data = _extract_level_data(level)
    with open(filename, 'w') as file:
        dump(data, file, indent=4)

@staticmethod
def _extract_level_data(level: Level) -> dict:
    """
    Extracts the relevant level data (index, position, attributes, key) into a dictionary.
    Returns:
        dict: A dictionary representing the level data.
    """
    rooms_data = []
    
    for room in level.map.values():
        room_data = {
            "index": room.index,
            "key": room.key,
            "x": room.position.x,
            "y": room.position.y,
            "attributes": [attr.name for attr in room.attributes]
        }
        rooms_data.append(room_data)
    
    return {
        "rooms": rooms_data
    }
