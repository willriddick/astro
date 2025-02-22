import pygame
from typing import Callable
from src.util import Vec2
from .button import Button
import src.assets as assets
from src.inputs import INPUTS
from src.sounds import SOUNDS


class InputButton(Button):

    INPUT_POS = Vec2(156, 4)

    def __init__(self, text: str, key: str, callback: Callable[[int], bool]):
        super().__init__(text, callback)
        self.key = key
        self.state = False
    
    @property
    def value(self) -> int:
        return INPUTS.get_input(self.key)
    
    @value.setter
    def value(self, value: int):
        INPUTS.set_input(self.key, value)
    
    def select(self):
        if not self.state:
            self.state = True
            SOUNDS.play('blip_pitch', pitch_index=-1 if self.state else 0)
            self.callback(False)
    
    def update(self, hovered):
        super().update(hovered)
        if self.state:
            if INPUTS.get('escape', just_pressed=True):
                self.state = False
                self.callback(True)  # enable menu movement
            else:
                new_value = INPUTS.get_next_keydown()
                if new_value and INPUTS.set_input(self.key, new_value):
                    self.value = new_value
                    self.state = False
                    self.callback(True)
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        
        item = '?' if self.state else pygame.key.name(self.value)
        surface.blit(assets.FONT.render(item, antialias=False, color=color), (self.INPUT_POS.x, 0))
        return surface
 