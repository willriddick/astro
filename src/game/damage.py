import pygame
from src.util import Vec2
from .collider import Collider

class DamageComponent:
    def __init__(self):
        self.collider = None
    
    def update(self, pos: Vec2):
        self.collider.update(pos)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        self.collider.render(display, offset)
    