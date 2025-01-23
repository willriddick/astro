import pygame
from .collider import Collider

class DamageComponent:
    def __init__(self):
        self.collider: Collider | None = None
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        self.collider.render(display, offset)
    