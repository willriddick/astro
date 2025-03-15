import pygame
from typing import Callable
from src.util import Vec2
from .button import Button
from src.sounds import SOUNDS
import src.graphics as graphics


class TextButton(Button):

    TEXT_POS = Vec2(132, 2)

    def __init__(self, text: str, callback: Callable[[bool], None]=None):
        super().__init__(text, callback)
        self.value = 'd8cxkjck'
        self.selected = False
    
    def select(self):
        self.selected = not self.selected
        SOUNDS.play('blip_pitch', pitch_index=-1 if self.value else 0)

        if self.callback:
            self.callback(self.value, self.selected)
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.selected else self.DEFAULT_COLOR
        surface.blit(graphics.FONT.render(self.value, antialias=False, color=color), self.TEXT_POS) 

        return surface
 