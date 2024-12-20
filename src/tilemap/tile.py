import pygame
from .tile_type import TileType

pygame.font.init()
FONT = pygame.font.Font('assets/DePixelIllegible.ttf', 8)

class Tile:
    def __init__(self, tilemap, type: TileType, variant: int, tile_pos: tuple[int, int]):
        self.tilemap = tilemap 
        self.type = type
        self.variant = variant
        self.tile_pos = tile_pos
        self.size = self.tilemap.tile_size
        self.pixel_pos = (tile_pos[0] * self.size, tile_pos[1] * self.size)
    
    def __str__(self):
        return f'{self.type}:{self.variant} ({self.tile_pos[0]}, {self.tile_pos[1]})'
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], self.size, self.size)
    
    def render(self, display: pygame.Surface, offset=(0, 0)):
        pos = (self.pixel_pos[0] - offset[0], self.pixel_pos[1] - offset[1])
        display.blit(self.type.images[self.variant], pos) 
        if self.tilemap.debug:
            text = FONT.render(f'{self.pixel_pos[0]}\n{self.pixel_pos[1]}', antialias=False, color=(255, 255, 255))
            display.blit(text, pos)