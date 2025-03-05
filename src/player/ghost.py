import pygame
from src.util import Vec2
from src.components import Entity
from .sprite import load_sprite

class Ghost(Entity):
    def __init__(self, palette_index=2):
        super().__init__(pygame.Vector2(0, 0), Vec2(8, 13))
        self.sprite = None
        self.palette_index = palette_index
        self.load_sprite(palette_index)

    def load_sprite(self, palette_index):
        self.palette_index = palette_index
        self.sprite, _ = load_sprite(palette_index)

    def update(self, new_pos=pygame.Vector2(0, 0)):
        self.position = self.position.lerp(new_pos, 0.5)
        self.sprite.update(self.position)
