import pygame
from .collider import Collider
from .health import HealthComponent

class DamageComponent:
    def __init__(self, damage: int):
        self.collider: Collider = None
        self.damage = damage
        self.nearest = None
        self.enabled = True
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)
        self.collider.enabled = self.enabled

        self.nearest = self.collider.get_nearest(
            lambda c: isinstance(c.owner, HealthComponent) and c.owner.enabled
        )
        if self.nearest:
            self.nearest.owner.take_damage(self.damage)
