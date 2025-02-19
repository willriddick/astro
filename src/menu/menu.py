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

        self.current_page: Page = None
        self.page_index = 0
        self.button_index = 0

        self.movement_enabled = True

        self.change_page(0)
    
    def change_page(self, page_index: int):
        self.page_index = page_index % len(self.pages)
        self.current_page = self.pages[self.page_index]
        self.button_index = self.current_page.index

    def update(self):
        if self.movement_enabled:
            input_dir = inputs.get_dir(just_pressed=True).y
            if input_dir:
                self.button_index = int((self.button_index + input_dir) % self.current_page.button_count)
                assets.SOUNDS.play('blip')

        if inputs.get('select', just_pressed=True):
            self.current_page.buttons[self.button_index].select()
    
    def render(self, display, _):
        for index, button in enumerate(self.current_page.buttons):
            button.update(hovered=index == self.button_index)
            surface = button.get_surface()
            y_pos = self.position.y + (index * button.SURFACE_SIZE.y)

            if self.draw_direction == 1:  # top-to-bottom
                y_pos = self.position.y + (index * button.SURFACE_SIZE.y)
            else:  # bottom-to-top
                y_pos = self.position.y - self.current_page.page_height + (index * button.SURFACE_SIZE.y)

            display.blit(surface, (self.position.x, y_pos))
