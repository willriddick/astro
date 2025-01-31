import pygame
from .collider import Collider

class DamageComponent:
    def __init__(self, collider: Collider, damage: int):
        self.collider = collider
        self.collider.add_owner(self)
        self.damage = damage
    
    def enable(self):
        self.collider.enabled = True

    def disable(self):
        self.collider.enabled = False
    
    @property
    def enabled(self) -> bool:
        return self.collider.enabled
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)
