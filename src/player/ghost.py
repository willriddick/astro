import pygame
from src.util import Vec2
from src.components import Entity

class Ghost(Entity):
    def __init__(self):
        super().__init__(pygame.Vector2(0, 0), Vec2(8, 13))
        pass

    def update(self, ):
        pass