import pygame
from .sprite import Sprite

class Entity:
    def __init__(self, level: 'Level', pos: pygame.Vector2):
        self.level = level
        self.pos = pos
        self.sprite: Sprite | None = None
    
    def update(self):
        pass

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        assert self.sprite, 'Sprite not set {self}'
        self.sprite.render(display, offset)
    
    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
    
    def get_pos(self) -> pygame.Vector2:
        return self.pos
    