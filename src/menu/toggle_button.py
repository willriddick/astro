import pygame
from typing import Callable
from src.util import Vec2
from .button import Button
import src.settings as settings
import src.assets as assets

class ToggleButton(Button):

    TOGGLE_POS = Vec2(156, 2)
    TOGGLE_SIZE = Vec2(8, 8)    

    def __init__(self, text: str, key: str, callback: Callable[[bool], None]=None):
        super().__init__(text, callback)
        self.key = key
    
    @property
    def value(self) -> int:
        return settings.get(self.key)
    
    @value.setter
    def value(self, value: int):
        settings.set_key(self.key, value)
    
    def select(self):
        self.value = not self.value
        assets.SOUNDS.play('blip_pitch', pitch_index=-1 if self.value else 0)
        if self.callback:
            self.callback(self.value)
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        pygame.draw.rect(
            surface, color, 
            rect=(
                self.TOGGLE_POS.x,
                self.TOGGLE_POS.y, 
                self.TOGGLE_SIZE.x, 
                self.TOGGLE_SIZE.y
            ), 
            width=1
        )

        if self.value:
            pygame.draw.rect(
                surface, color, 
                rect=(
                    self.TOGGLE_POS.x + 2, 
                    self.TOGGLE_POS.y + 2, 
                    self.TOGGLE_SIZE.x - 4, 
                    self.TOGGLE_SIZE.y - 4
                )
            )

        return surface
 