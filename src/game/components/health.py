import pygame
from src.util import Timer
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
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer.is_done
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer.is_active
    
    def enable(self):
        self.collider.enabled = True

    def disable(self):
        self.collider.enabled = False
    
    @property
    def enabled(self) -> bool:
        return self.collider.enabled

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
