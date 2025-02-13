import pygame
from src.util import Assets, Vec2
from .button import Button

class Menu():
    def __init__(self, pages: list[list[Button]], position = Vec2(16, 16), draw_direction = -1):
        self.pages = pages
        self.position = position
        self.draw_direction = draw_direction

        self.input_dir = pygame.Vector2(0, 0)
        self.input_select = False 
        self.input_back = False 

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
        self.get_input()
        self.hovered_index = int((self.hovered_index + self.input_dir.y) % len(self.current_buttons))

        if self.input_dir.y != 0:
            Assets.SOUNDS.play('blip')

        if self.input_select:
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

    def get_input(self):
        just_pressed = pygame.key.get_just_pressed()
        self.input_dir = pygame.Vector2(
            int(just_pressed[pygame.K_d]) - int(just_pressed[pygame.K_a]),
            int(just_pressed[pygame.K_s]) - int(just_pressed[pygame.K_w])
        )
        self.input_select = just_pressed[pygame.K_RETURN]
