import pygame
from src.util import Assets, Vec2
from .button import Button
from src.game.input import Input

class Menu():
    def __init__(self, pages: list[list[Button]], position = Vec2(16, 16), draw_direction = -1):
        self.pages = pages
        self.position = position
        self.draw_direction = draw_direction

        self.input = Input()
        self.movement_enabled = True

        self.selected_page = 0
        self.hovered_index = 0
        self.current_buttons: list[Button] = []
        self.page_height = 0

        self.change_page(0)
    
    def change_page(self, page_index: int):
        self.selected_page = page_index % len(self.pages)
        self.hovered_index = 0
        self.current_buttons = self.pages[self.selected_page]
        self.page_height = len(self.current_buttons) * self.current_buttons[0].SURFACE_SIZE.y

    def update(self):
        if self.movement_enabled:
            input_dir = self.input.get_dir(just_pressed=True).y
            if input_dir:
                self.hovered_index = int((self.hovered_index + input_dir) % len(self.current_buttons))
                Assets.SOUNDS.play('blip')

        if self.input.get('select', just_pressed=True):
            self.current_buttons[self.hovered_index].select()
    
    def render(self, display, _):
        for index, button in enumerate(self.current_buttons):
            button.update(hovered=index == self.hovered_index)
            surface = button.get_surface()
            y_pos = self.position.y + (index * button.SURFACE_SIZE.y)

            if self.draw_direction == 1:  # top-to-bottom
                y_pos = self.position.y + (index * button.SURFACE_SIZE.y)
            else:  # bottom-to-top
                y_pos = self.position.y - self.page_height + (index * button.SURFACE_SIZE.y)

            display.blit(surface, (self.position.x, y_pos))
