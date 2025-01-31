import pygame
from .sprite import Sprite

class Entity:
    def __init__(self, pos: pygame.Vector2):
        self.pos = pos
        self.sprite: Sprite | None = None
    
    def update(self) -> None:
        pass

    def render(self, display: pygame.Surface, offset: pygame.Vector2) -> None:
        if self.sprite:
            self.sprite.render(display, offset)
    
    def set_pos(self, pos: pygame.Vector2) -> None:
        self.pos = pos
    
    def get_pos(self) -> pygame.Vector2:
        return self.pos
    