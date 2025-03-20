import asyncio
import inspect
import random
import pygame
from src.util import Vec2
from src.clock import CLOCK
from src.camera import CAMERA
from src.sounds import SOUNDS
import src.graphics as graphics


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

        self.DEFAULT_COLOR = graphics.PALETTE[6]
        self.DISABLED_COLOR = graphics.PALETTE[4]

        if Button.HOVERED_COLOR is None:
            Button.HOVERED_COLOR = graphics.PALETTE[random.choice([
                random.randint(24, 26),
                random.randint(28, 31),
                random.randint(34, 37),
                random.randint(41, 44),
                random.randint(47, 48),
                random.randint(55, 61)
            ])]
    
    def __str__(self):
        return self.text
   
    def select(self):
        SOUNDS.play('select')
        CAMERA.screenshake(30, 1)

        if self.callback:
            if inspect.iscoroutinefunction(self.callback):
                asyncio.create_task(self.callback())  # Run async function in background
            else:
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
        surface.blit(graphics.FONT.render(self.text, antialias=False, color=color), (self.x_offset, 0))
        return surface
