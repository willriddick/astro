import pygame
from .collider import Collider
from .health import HealthComponent

class DamageComponent:
    def __init__(self, collider: Collider, damage: int):
        self.collider = collider
        self.collider.add_owner(self)
        self.damage = damage
        self.nearest = None
    
    def enable(self):
        self.collider.enabled = True

    def disable(self):
        self.collider.enabled = False
    
    @property
    def enabled(self) -> bool:
        return self.collider.enabled
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)

        self.nearest: HealthComponent = self.collider.get_nearest(HealthComponent)
        if self.nearest:
            self.nearest.apply_damage(self.damage)
