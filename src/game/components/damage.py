import pygame
from .collider import Collider
from .health import HealthComponent

class DamageComponent:
    def __init__(self, damage: int):
        self.collider: Collider | None = None
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

        self.nearest = self.collider.get_nearest(
            lambda c: isinstance(c.owner, HealthComponent) and c.owner.enabled
        )
        if self.nearest:
            self.nearest.owner.apply_damage(self.damage)
