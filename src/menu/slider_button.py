import pygame
from typing import Callable
from src.util import Vec2
from src.clock import CLOCK
from src.settings import SETTINGS
from src.inputs import INPUTS
import src.assets as assets
from .button import Button

class SliderButton(Button):

    SLIDER_LENGTH = 64
    SLIDER_POS = Vec2(96, 4)
    KNOB_SIZE = Vec2(3, 7)
    KNOB_SPEED = 20

    def __init__(self, text: str, key: str, callback: Callable[[int], None]=None, min_value=0, max_value=10, step=1, wrap=True):
        super().__init__(text, callback)
        self.key = key
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.wrap = wrap

        self.knob_position = 0
        self.knob_target = 0
    
    @property
    def value(self) -> int:
        return SETTINGS.get(self.key)
    
    @value.setter
    def value(self, value: int):
        SETTINGS.set_key(self.key, value)
    
    def select(self):
        self.change_value(self.value * self.step)
    
    def change_value(self, value: int):
        """Update the slider value while respecting min/max bounds."""
        value_range = self.max_value - self.min_value + 1
        if self.wrap:
            self.value = (value * self.step - self.min_value) % value_range + self.min_value
        else:
            self.value = max(self.min_value, min(self.max_value, value))

        assets.SOUNDS.play('blip_pitch', pitch_index=self.value)
        if self.callback:
            self.callback(self.value)
    
    def update(self, hovered: bool):
        super().update(hovered)
        if self.hovered:
            input_dir = INPUTS.get_dir(just_pressed=True).x
            if input_dir != 0:
                self.change_value(self.value + input_dir)

        # Adjust slider knob positioning based on min_value
        self.knob_target = self.SLIDER_LENGTH * ((self.value - self.min_value) / (self.max_value - self.min_value))
        self.knob_position += (self.knob_target - self.knob_position) * self.KNOB_SPEED * CLOCK.dt
 
    def get_surface(self) -> pygame.Surface:
        surface = super().get_surface()

        if self.disabled:
            color = self.DISABLED_COLOR
        else:
            color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR

        pygame.draw.line(
            surface, color, 
            start_pos=self.SLIDER_POS, 
            end_pos=(self.SLIDER_POS.x + self.SLIDER_LENGTH, self.SLIDER_POS.y),
            width=1
        )
        pygame.draw.rect(
            surface, color, 
            rect=(
                self.SLIDER_POS.x + self.knob_position, 
                self.SLIDER_POS.y - self.KNOB_SIZE.y // 2, 
                self.KNOB_SIZE.x, 
                self.KNOB_SIZE.y
            ),
            width=1
        )
        return surface
