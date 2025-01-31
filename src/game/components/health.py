import pygame
from src.util import Timer
from .damage import DamageComponent
from .entity import Entity
from .collider import Collider

class HealthComponent(Entity):
    def __init__(self, collider: Collider, max_health: int, invulnerable_duration: int = 500):
        self.collider = collider
        self.collider.add_owner(self)
        self.max_health = max_health
        self.health = max_health
        self.invulnerable_duration = invulnerable_duration
        self.invulnerable_timer = Timer(invulnerable_duration)

        self.on_death = lambda: None
        self.on_damaged = lambda: None
    
    def update(self, position: pygame.Vector2):
        self.collider.update(position)

        self.nearest = self.collider.get_nearest(DamageComponent)
        if self.nearest:
            self.apply_damage(self.nearest.damage)

    def enable(self):
        self.collider.enabled = True

    def disable(self):
        self.collider.enabled = False
    
    @property
    def enabled(self) -> bool:
        return self.collider.enabled
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer.is_done
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer.is_active

    def reset(self):
        self.health = self.max_health
  
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        
    def apply_damage(self, amount: int):
        if self.vulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable_timer.start()
            self.on_damaged()

            if self.health == 0:
                self.on_death()
