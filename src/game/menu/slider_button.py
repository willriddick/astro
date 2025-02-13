import pygame
from typing import Callable
from src.util import Vec2
from .button import Button

class SliderButton(Button):

    SLIDER_LENGTH = 64
    SLIDER_POS = Vec2(96, 4)
    KNOB_SIZE = Vec2(3, 5)

    def __init__(self, text: str, callback: Callable[[int], None], value: int = 5, max_value: int = 10):
        super().__init__(text, callback)
        self.value = value
        self.max_value = max_value

        self.knob_position = 0
        self.knob_target = 0
    
    def select(self):
        self.value = (self.value + 1) % (self.max_value + 1)
        self.callback(self.value)
    
    def update(self, hovered: bool):
        super().update(hovered)
        self.knob_target = self.SLIDER_LENGTH * (self.value / self.max_value)
        self.knob_position += (self.knob_target - self.knob_position) * 0.2
    
    def get_surface(self) -> pygame.Surface:
        surface = super().get_surface()
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        pygame.draw.line(
            surface, color, 
            start_pos=self.SLIDER_POS, 
            end_pos=(self.SLIDER_POS.x + self.SLIDER_LENGTH, self.SLIDER_POS.y),
            width=1
        )
        pygame.draw.rect(
            surface, color, 
            rect=pygame.Rect(
                self.SLIDER_POS.x + self.knob_position, 
                self.SLIDER_POS.y - self.KNOB_SIZE.y // 2, 
                self.KNOB_SIZE.x, 
                self.KNOB_SIZE.y
            )
        )
        return surface
