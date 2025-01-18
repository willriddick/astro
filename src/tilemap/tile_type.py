import pygame
from src.util import Vec2

class TileType:
    def __init__(self, name: str, images: list[pygame.Surface], autotile: bool = False, size: Vec2=Vec2(16, 16)):
        self.name = name
        self.images = images
        self.autotile = autotile
        self.size = size
