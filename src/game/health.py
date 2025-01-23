import pygame
from src.util import Vec2
from .collider import Collider
from .damage import DamageComponent

class HealthComponent:
    def __init__(self, max_health: int, invulnerable_duration: int = 30):
        self.max_health = max_health
        self.collider: Collider | None = None
        self.health = max_health
        self.invulnerable_duration = invulnerable_duration
        self.invulnerable_timer = 0
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer == 0
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer > 0
    
    def update(self, pos: pygame.Vector2, colliders: list[Collider]):
        self.collider.update(pos)
        self.invulnerable_timer = max(0, self.invulnerable_timer - 1)

        if self.vulnerable and self.collider.get_nearest(
            colliders, 
            lambda c: type(c.owner) is DamageComponent
        ):
            self.take_damage(1)
    
    def reset(self):
        self.health = self.max_health
  
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        
    def take_damage(self, amount: int):
        if self.vulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable_timer = self.invulnerable_duration

            if self.health == 0:
                self.on_death()
    
    def on_death(self):
        self.reset()
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        self.collider.render(display, offset)
