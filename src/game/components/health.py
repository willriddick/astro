import pygame
from .collider import Collider

class HealthComponent:
    def __init__(self, max_health: int, invulnerable_duration: int = 30):
        self.max_health = max_health
        self.collider: Collider | None = None
        self.health = max_health
        self.invulnerable_duration = invulnerable_duration
        self.invulnerable_timer = 0

        self.enabled = True

        self.on_death = lambda: None
        self.on_damaged = lambda: None
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer == 0
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer > 0

    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def update(self, pos: pygame.Vector2):
        self.collider.update(pos)
        self.invulnerable_timer = max(0, self.invulnerable_timer - 1)
        self.collider.enabled = self.enabled

    def reset(self):
        self.health = self.max_health
  
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        
    def take_damage(self, amount: int):
        if self.vulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable_timer = self.invulnerable_duration
            self.on_damaged()

            if self.health == 0:
                self.on_death()
