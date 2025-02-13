import pygame
from typing import Callable
from .button import Button

class ToggleButton(Button):
    def __init__(self, text: str, callback: Callable[[bool], None], state=False):
        super().__init__(text, callback)
        self.state = state
    
    def select(self):
        self.state = not self.state
        self.callback(self.state)
 