import pygame
from typing import Callable
from src.util import Assets, Vec2
from .button import Button

class ToggleButton(Button):

    TOGGLE_POS = Vec2(156, 4)
    TOGGLE_SIZE = Vec2(8, 8)    

    def __init__(self, text: str, callback: Callable[[bool], None], state=False):
        super().__init__(text, callback)
        self.state = state
    
    def select(self):
        self.state = not self.state
        Assets.SOUNDS.play('pitch_blip', pitch_index=Assets.SOUNDS.get('pitch_blip').get_count() if self.state else 0)
        self.callback(self.state)
    
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

        if self.state:
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
 