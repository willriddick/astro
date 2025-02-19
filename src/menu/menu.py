from src.util import Vec2
import src.assets as assets
import src.inputs as inputs
from .button import Button
from .page import Page

class Menu():
    def __init__(self, pages: list[Page], position = Vec2(16, 16), draw_direction = -1):
        self.pages = pages
        self.position = position
        self.draw_direction = draw_direction
        self.movement_enabled = True

        self.current_page: Page = None
        self.page_index = 0
        self.change_page(self.page_index)

    def change_page(self, page_index: int):
        self.page_index = page_index % len(self.pages)
        self.current_page = self.pages[self.page_index]

    def update(self):
        if self.movement_enabled:
            input_dir = inputs.get_dir(just_pressed=True).y
            if input_dir:
                self.current_page.move_index(input_dir)
                assets.SOUNDS.play('blip')

        if inputs.get('select', just_pressed=True):
            self.current_page.selected_button.select()
    
    def render(self, display, _):
        self.current_page.render(display, self.position, self.draw_direction)