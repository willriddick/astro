import pygame
from .tile_type import TileType
from src.util import Vec2

class TileSet:
    def __init__(self, tile_size: Vec2):
        self.tileset: list[TileType] = []
        self.tile_size = tile_size
    
    def add(self, name: str, images: list[pygame.Surface], autotile: bool = False):
        self.tileset.append(TileType(name, images, autotile, self.tile_size))
    
    def get_by(self, name: str) -> TileType:
        for tile in self.tileset:
            if tile.name == name:
                return tile
        raise ValueError(f'Tile "{name}" not found in tileset')
    
    def get_by_index(self, index: int) -> TileType:
        return self.tileset[index % len(self.tileset)]
