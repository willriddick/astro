from random import randint
import pygame
from src.util import Vec2
from src.clock import CLOCK
import src.assets as assets
from src.camera import CAMERA

class Button():

    SURFACE_SIZE = Vec2(224, 16)
    X_OFFSET = 7
    OFFSET_SPEED = 15 

    HOVERED_COLOR = None  # placeholder 

    def __init__(self, text: str, callback: callable):
        self.text = text
        self.callback = callback
        self.hovered = False
        self.x_offset = 0
        self.target_offset = 0 

        self.disabled = False

        self.DEFAULT_COLOR = assets.PALETTE[5]
        self.DISABLED_COLOR = assets.PALETTE[3]

        if Button.HOVERED_COLOR is None:
            Button.HOVERED_COLOR = assets.PALETTE[randint(20, len(assets.PALETTE) - 1)]
    
    def __str__(self):
        return self.text
   
    def select(self):
        assets.SOUNDS.play('select')
        CAMERA.screenshake(30, 1)
        self.callback()
    
    def update(self, hovered: bool):
        self.hovered = hovered
        self.target_offset = self.X_OFFSET if self.hovered else 0
        self.x_offset += (self.target_offset - self.x_offset) * self.OFFSET_SPEED * CLOCK.dt
    
    def get_surface(self) -> pygame.Surface:
        if self.disabled:
            color = self.DISABLED_COLOR
        else:
            color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR

        surface = pygame.Surface(self.SURFACE_SIZE, pygame.SRCALPHA)
        surface.blit(assets.FONT.render(self.text, antialias=False, color=color), (self.x_offset, 0))
        return surface
