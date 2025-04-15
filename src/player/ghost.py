import pygame
from src.util import Vec2
from src.components import Entity
from src.settings import SETTINGS
import src.graphics as graphics
from .enums import Animations
from .sprite import load_sprite

class Ghost(Entity):

    TAG_OFFSET = Vec2(4, -16)
    TAG_ALPHA = 100

    def __init__(self, username: str, palette_index=2):
        super().__init__(pygame.Vector2(0, 0), Vec2(8, 13))
        self.username = username
        self.sprite = None
        self.palette_index = palette_index
        self.load_sprite(palette_index)

        self.TAG_COLOR = graphics.PALETTE[6]
        self.TAG_SURF = graphics.FONT.render(self.username, antialias=False, color=(255, 255, 255))
        self.TAG_SURF.set_alpha(self.TAG_ALPHA)
        self.TAG_WIDTH = self.TAG_SURF.get_width()

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
    
    def render(self, display, offset):
        super().render(display, offset)

        if SETTINGS.get("show_gamertag"):
            display.blit(
                self.TAG_SURF, 
                (
                    self.position.x + self.TAG_OFFSET.x - self.TAG_WIDTH // 2 + offset.x, 
                    self.position.y + self.TAG_OFFSET.y + offset.y
                )
            )
    