import pygame
from typing import Callable
from src.util import Assets, Vec2
from src.game.input import Input
from .button import Button

class InputButton(Button):

    INPUT_POS = Vec2(156, 4)

    def __init__(self, text: str, callback: Callable[[int], bool], value: int):
        super().__init__(text, callback)
        self.value = value
        self.state = False
        self.input = Input()
    
    def select(self):
        if not self.state:
            self.state = True
            Assets.SOUNDS.play('blip_pitch', pitch_index=-1 if self.state else 0)
            self.callback(self.value)
    
    def update(self, hovered):
        super().update(hovered)
        if self.state:
            if self.input.get('escape', just_pressed=True):
                self.callback(self.value)
                self.state = False
            else:
                key = self.input.get_next_keydown()
                if self.callback(key):
                    self.value = key
                    self.state = False
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        
        item = '?' if self.state else pygame.key.name(self.value)
        surface.blit(Assets.FONT.render(item, antialias=False, color=color), (self.INPUT_POS.x, 0))
        return surface
 