import re
import pygame
from typing import Callable
from src.util import Vec2
from .button import Button
from src.sounds import SOUNDS
from src.inputs import INPUTS
import src.graphics as graphics

ALLOWED_CHARACTERS = re.compile(r'[a-zA-Z0-9_]')


class TextButton(Button):

    TEXT_POS = Vec2(116, 2)

    def __init__(self, text: str, callback: Callable[[bool], None]=None):
        super().__init__(text, callback)
        self.value = ''
        self.selected = False
    
    def update(self, hovered: bool):
        super().update(hovered)
        if self.selected:
            key = INPUTS.get_next_keydown()
            if key:
                char = pygame.key.name(key)
                if key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]  # Remove last character
                elif len(char) == 1 and ALLOWED_CHARACTERS.match(char):
                    if len(self.value) < 12:
                        self.value += char
                
    def select(self):
        self.selected = not self.selected
        SOUNDS.play('blip_pitch', pitch_index=-1 if self.value else 0)

        if self.callback:
            self.callback(self.selected, self.value)
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.selected else self.DEFAULT_COLOR
        
        if self.value == '' and not self.selected:
            text = '_____________'
        else:
            text = self.value 

        surface.blit(graphics.FONT.render(text, antialias=False, color=color), self.TEXT_POS) 
        return surface
 