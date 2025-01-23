import pygame
from .collider import Collider

class DamageComponent:
    def __init__(self, damage: int):
        self.collider: list[Collider] = []
        self.damage = damage
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)
