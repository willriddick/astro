import pygame
from .sprite import Sprite
from src.util import Vec2

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, rect_size: Vec2):
        super().__init__()
        self.pos = pos
        self.rect_size = rect_size
        self.sprite: Sprite | None = None
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        assert self.sprite, 'Sprite not set {self}'
        self.sprite.render(display, offset)
    
    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
    
    def get_pos(self) -> pygame.Vector2:
        return self.pos
    
    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    @property
    def rect(self) -> pygame.FRect:
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size.x, self.rect_size.y)
