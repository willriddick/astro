import pygame
from src.util import Vec2


class TileType:
    """
    Represents a type of tile that can be placed on a tilemap.

    Args:
        name (str): The name of the tile type.
        images (list[pygame.Surface]): A list of images that represent the tile.
        autotile (bool): Whether the tile should be autotiled.
        size (Vec2): The size of the tiles collision box.
        collision (bool): Whether the tile should have collision.
        collision_offset (Vec2): The offset of the collision box from the top-left corner of the tile.
    """
    def __init__(self, 
            name: str,
            images: list[pygame.Surface],
            size: Vec2=Vec2(16, 16),
            autotile: bool = False,
            collision: bool = False,
            collision_offset: Vec2 = Vec2(0, 0),
        ):
        self.name = name
        self.images = images
        self.autotile = autotile
        self.size = size
        self.collision = collision
        self.collision_offset = collision_offset
