import pygame
from ..util import approach
import numpy as np

class Camera():
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.display = pygame.Surface((width, height))
        self.offset = pygame.Vector2(0, 0)
    
    def update(self):
        self.display.fill((0, 0, 0))
   
    def move_to(self, target: pygame.Vector2, alpha: float=0.2):
        target = self.get_center(target)
        cos_alpha = (1 - np.cos(alpha * np.pi)) / 2
        self.offset = self.offset * (1 - cos_alpha) + target * cos_alpha

    def get_center(self, target: pygame.Vector2):
        return pygame.Vector2(target.x - self.width // 2, target.y - self.height // 2)
    