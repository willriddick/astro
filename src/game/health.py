import pygame
from src.util import Vec2
from .collider import Collider

class HealthComponent:
    def __init__(self, max_health: int, collider: Collider, invulnerable_duration: int = 15):
        self.max_health = max_health
        self.collider = collider
        self.health = max_health
        self.invulnerable_duration = invulnerable_duration
        self.invulnerable_timer = 0
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer == 0
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer > 0
    
    def update(self, pos: Vec2, colliders: list[Collider]):
        self.collider.update(pos, colliders)
        print(self.collider.nearest)

        self.invulnerable_timer = max(0, self.invulnerable_timer - 1)
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        self.collider.render(display, offset)
    
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        
    def take_damage(self, amount: int):
        if self.vulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable_timer = self.invulnerable_duration

            if self.health == 0:
                self.on_death()
