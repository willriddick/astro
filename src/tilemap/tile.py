import pygame
from .tile_type import TileType
from src.util import Vec2

class Tile:
    def __init__(self, tilemap, type: TileType, variant: int, tile_pos: Vec2):
        self.tilemap = tilemap 
        self.type = type
        self.variant = variant
        self.tile_pos = tile_pos
    
    def __str__(self):
        return f'{self.type.name}:{self.variant} {self.tile_pos}'
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def pixel_pos(self) -> Vec2:
        return Vec2(
            self.tile_pos.x * self.type.size.x, 
            self.tile_pos.y * self.type.size.y
        ) 
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.pixel_pos.x,
            self.pixel_pos.y,
            self.type.size.x,
            self.type.size.y
        )
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        pos = (self.pixel_pos.x - offset.x, self.pixel_pos.y - offset.y)
        display.blit(self.type.images[self.variant], pos)
