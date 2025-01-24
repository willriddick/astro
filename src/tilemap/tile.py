import pygame
from src.util import Vec2
from .tile_type import TileType

class Tile:
    def __init__(self, tilemap, tile_type: TileType, variant: int, tile_pos: Vec2):
        self.tilemap = tilemap 
        self.tile_type = tile_type
        self.variant = variant
        self.tile_pos = tile_pos
        self.collision = self.tile_type.collision
        self.debug = False

    def __str__(self):
        return f'{self.tile_type.name}:{self.variant} {self.tile_pos}'
    
    def __repr__(self):
        return self.__str__()

    @property
    def tile_size(self) -> Vec2:
        return self.tilemap.tile_size
    
    @property
    def pos(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.tile_pos.x * self.tile_size.x,
            self.tile_pos.y * self.tile_size.y
        ) 
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.pos.x + self.tile_type.collision_offset.x,
            self.pos.y + self.tile_type.collision_offset.y,
            self.tile_type.size.x,
            self.tile_type.size.y
        )
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        if len(self.tile_type.images) == 0:
            return

        pos = (self.pos.x - offset.x, self.pos.y - offset.y)
        display.blit(self.tile_type.images[self.variant], pos)

        if self.debug and self.collision:
            size = self.tile_type.size
            collision_display = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
            collision_display.set_alpha(100)
            pygame.draw.rect(
                collision_display, (255, 0, 255),
                (0, 0, size.x, size.y), 1
            )
            display.blit(
                collision_display, 
                (self.pos.x - offset.x, self.pos.y - offset.y)
            )
