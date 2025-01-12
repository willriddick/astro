import pygame
from .tile_type import TileType

pygame.font.init()
FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)

class Tile:
    def __init__(self, tilemap, type: TileType, variant: int, tile_pos: tuple[int, int]):
        self.tilemap = tilemap 
        self.type = type
        self.variant = variant
        self.tile_pos = tile_pos
    
    def __str__(self):
        return f'{self.type.name}:{self.variant} ({self.tile_pos[0]}, {self.tile_pos[1]})'
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def pixel_pos(self) -> tuple[int, int]:
        return (self.tile_pos[0] * self.tilemap.tileset.tile_size, self.tile_pos[1] * self.tilemap.tileset.tile_size) 
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], self.tilemap.tileset.tile_size, self.tilemap.tileset.tile_size)
    
    def render(self, display: pygame.Surface, offset=(0, 0)):
        pos = (self.pixel_pos[0] - offset[0], self.pixel_pos[1] - offset[1])
        display.blit(self.type.images[self.variant], pos) 
        if self.tilemap.debug:
            text = FONT.render(f'{self.pixel_pos[0]}\n{self.pixel_pos[1]}', antialias=False, color=(255, 255, 255))
            display.blit(text, pos)