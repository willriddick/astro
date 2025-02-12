from typing import Callable
import pygame
from src.util.assets import Assets

class Button():

    def __init__(self, text: str, callback: callable):
        self.text = text
        self.callback = callback
        self.hovered = False
        self.x_offset = 0
        self.target_offset = 0 

        self.HOVERED_COLOR = Assets.PALETTE[34]
        self.DEFAULT_COLOR = Assets.PALETTE[5]
    
    def __str__(self):
        return self.text
   
    def select(self):
        self.callback()
    
    def get_surface(self) -> pygame.Surface:
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        return Assets.FONT.render(f'{self}', antialias=False, color=color)
    
    def update(self):
        self.x_offset += (self.target_offset - self.x_offset) * 0.2

class ToggleButton(Button):
    def __init__(self, text: str, callback: Callable[[bool], None], state=False):
        super().__init__(text, callback)
        self.state = state
    
    def select(self):
        self.state = not self.state
        self.callback(self.state)
    
    def __str__(self):
        return self.text + ('  [ON]' if self.state else '  [OFF]')
    
class SliderButton(Button):
    def __init__(self, text: str, callback: Callable[[int], None], value: int = 5, max_value: int = 10):
        super().__init__(text, callback)
        self.value = value
        self.max_value = max_value
    
    def select(self):
        self.value = (self.value + 1) % (self.max_value + 1)
        self.callback(self.value)
    
    def __str__(self):
        return f'{self.text}   [{self.value}]'
