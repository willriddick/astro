import pygame
import numpy as np
from .entity import Entity

class Camera:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display = pygame.Surface((width, height))
        self.offset = pygame.Vector2(0, 0)

        self.target: Entity = None
        self.entities: list[Entity] = []
    
    def update(self):
        self.display.fill((0, 0, 0))

        if self.target:
            self.move_to(self.target.get_center())

        for entity in self.entities:
            entity.render(self.display, -self.offset)
    
    def set_target(self, target: Entity):
        if target not in self.entities:
            self.add(target)
        self.target = target
    
    def add(self, entity: Entity):
        self.entities.append(entity)
   
    def remove(self, entity: Entity):
        if self.target == entity:
            self.target = None
        self.entities.remove(entity)
   
    def move_to(self, target: pygame.Vector2, smoothing: float = 0.2):
        target_offset = pygame.Vector2(target.x - self.width // 2, target.y - self.height // 2)
        cos_smoothing = (1 - np.cos(smoothing * np.pi)) / 2
        self.offset = self.offset * (1 - cos_smoothing) + target_offset * cos_smoothing
