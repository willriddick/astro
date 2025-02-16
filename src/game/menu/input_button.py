import pygame
from typing import Callable
from src.util import Assets, Vec2
from src.game.input import Input
from .button import Button

class InputButton(Button):

    INPUT_POS = Vec2(156, 4)

    def __init__(self, text: str, callback: Callable[[int], bool], key: int):
        super().__init__(text, callback)
        self.key = key
        self.state = False
        self.input = Input()
    
    def select(self):
        self.state = True
        Assets.SOUNDS.play('blip', pitch_index=Assets.SOUNDS.get('pitch_blip').get_count() if self.state else 0)
        self.callback(self.key)
        print(self.state)
    
    def update(self, hovered):
        super().update(hovered)
        if self.state:
            if self.input.get('escape', just_pressed=True):
                self.state = False

            key = self.input.get_next_keydown()
            if self.callback(key):
                self.key = key  
                self.state = False
    
    def get_surface(self):
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        
        item = '?' if self.state else pygame.key.name(self.key)
        surface.blit(Assets.FONT.render(item, antialias=False, color=color), (self.INPUT_POS.x, 0))
        return surface
 