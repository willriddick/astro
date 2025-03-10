import pygame
from src.util import Vec2
from src.components import Entity
from .enums import Animations
from .sprite import load_sprite

class Ghost(Entity):
    def __init__(self, username: str, palette_index=2):
        super().__init__(pygame.Vector2(0, 0), Vec2(8, 13))
        self.username = username
        self.sprite = None
        self.palette_index = palette_index
        self.load_sprite(palette_index)

    def load_sprite(self, palette_index):
        self.palette_index = palette_index
        self.sprite, _ = load_sprite(palette_index)

    def update(self, new_pos: pygame.Vector2, current_anim: int, flip_x: bool, flash: bool, alpha: bool):
        self.position = self.position.lerp(new_pos, 0.5)
        self.sprite.update(self.position)
        self.sprite.set_animation(Animations(current_anim))
        self.sprite.flip_x = flip_x
        if flash:
            self.sprite.flash(100)
        if alpha:
            self.sprite.oscillate_alpha(100)
    