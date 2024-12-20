import pygame

class Asset:
    def __init__(self, name: str, images: list[pygame.Surface], autotile: bool = False, tile_size: int = 16):
        self.name = name
        self.tile_size = tile_size
        self.images = images
        self.autotile = autotile
