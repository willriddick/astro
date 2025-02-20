import pygame
from src.clock import Clock
from src.util import Vec2, Timer
import src.assets as assets
import src.inputs as inputs
from .page import Page

class Menu():

    def __init__(self, pages: list[Page], position=Vec2(16, 16), draw_direction=-1, transition_duration=200):
        self.pages = pages
        self.position = position
        self.draw_direction = draw_direction
        self.movement_enabled = True

        self.transition_timer = Timer()
        self.transition_duration = transition_duration

        self.page_index = 0
        self.current_page: Page = self.pages[self.page_index]
        self.previous_page: Page = None

    def change_page(self, page_index: int):
        self.previous_page = self.current_page
        self.page_index = page_index % len(self.pages)
        self.current_page = self.pages[self.page_index]
        self.transition_timer.start(self.transition_duration)

    def update(self):
        if self.movement_enabled:
            input_dir = inputs.get_dir(just_pressed=True).y
            if input_dir:
                self.current_page.change_index(input_dir)
                assets.SOUNDS.play('blip')

        if inputs.get('select', just_pressed=True):
            self.current_page.selected_button.select()
    
    def render(self, display, _):
        if self.transition_timer.is_active:
            self._render_transition(display) 
        else:
            self.current_page.render(display, self.position, self.draw_direction, 255)
    
    def _render_transition(self, display):
        progress = self.transition_timer.progress
        self.previous_page.render(display, self.position, self.draw_direction, int((1 - progress) * 255))
        self.current_page.render(display, self.position, self.draw_direction, int(progress * 255))
    