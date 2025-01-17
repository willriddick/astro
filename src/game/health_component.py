import pygame
from src.util import Vec2

class HealthComponent:
    def __init__(self, max_health: int, rect_size: Vec2, invulnerable_duration: int = 15):
        self.max_health = max_health
        self.health = max_health
        self.invulnerable_duration = invulnerable_duration
        self.invulnerable_timer = 0
        self.rect = pygame.Rect(0, 0, rect_size.x, rect_size.y)
    
    @property
    def vulnerable(self):
        return self.invulnerable_timer == 0
    
    @property
    def invulnerable(self):
        return self.invulnerable_timer > 0
    
    def update(self, pos: Vec2, colliders: list):
        self.rect.topleft = pos

        self.invulnerable_timer = max(0, self.invulnerable_timer - 1)

        if self.rect.collidelist(colliders):
            self.take_damage(colliders[0].damage)
    
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        
    def take_damage(self, amount: int):
        if self.vulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable_timer = self.invulnerable_duration

            if self.health == 0:
                self.on_death()
