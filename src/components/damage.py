import pygame
from .collider import Collider


class DamageComponent:
    def __init__(self, colliders: Collider | list[Collider], damage: int):
        self.colliders = colliders if isinstance(colliders, list) else [colliders]
        for collider in self.colliders:
            collider.add_owner(self)
        self.damage = damage
        self.enabled = True
    
    def update(self, position: pygame.Vector2):
        for collider in self.colliders:
            collider.update(position)
    
    def enable(self):
        self.enabled = True
        for collider in self.colliders:
            collider.enabled = True

    def disable(self):
        self.enabled = False
        for collider in self.colliders:
            collider.enabled = False
    