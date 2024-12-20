import pygame
from .asset import Asset

pygame.font.init()
FONT = pygame.font.Font('assets/DePixelIllegible.ttf', 8)

class Tile:
    def __init__(self, tilemap, asset: Asset, variant: int, tile_pos: tuple[int, int]):
        self.tilemap = tilemap 
        self.asset = asset
        self.variant = variant
        self.tile_pos = tile_pos
        self.size = self.tilemap.tile_size
        self.pixel_pos = (tile_pos[0] * self.size, tile_pos[1] * self.size)
    
    def __str__(self):
        return f'{self.type}:{self.variant} ({self.tile_pos[0]}, {self.tile_pos[1]})'
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], self.size, self.size)
    
    def render(self, surf: pygame.Surface, offset=(0, 0)):
        pos = (self.pixel_pos[0] - offset[0], self.pixel_pos[1] - offset[1])
        surf.blit(self.asset.images[self.variant], pos)
        if self.tilemap.debug:
            text = FONT.render(f'{self.pixel_pos[0]}\n{self.pixel_pos[1]}', antialias=False, color=(255, 255, 255))
            surf.blit(text, pos)