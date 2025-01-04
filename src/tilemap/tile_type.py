import pygame

class TileType:
    def __init__(self, name: str, images: list[pygame.Surface], autotile: bool = False):
        self.name = name
        self.images = images
        self.autotile = autotile
