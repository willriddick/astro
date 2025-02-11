import pygame
from src.util import State, Assets
from .game_states import GameStates

class Menu(State):
    def __init__(self):
        super().__init__(GameStates.MENU)

        self.input_dir = pygame.Vector2(0, 0)
        self.input_select = False 
        self.input_back = False 

        self.buttons = ['Play', 'Settings', 'Quit']
        self.selected_index = 0

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        self.owner.camera.set_render_callback(self.render)
        self.get_input()
        self.selected_index = (self.selected_index + self.input_dir.y) % len(self.buttons)

        if self.input_select:
            match self.selected_index:
                case 0:
                    self.owner.state_machine.switch(GameStates.PLAYING)
                case 1:
                    self.owner.state_machine.switch(GameStates.SETTINGS)
                case 2:
                    self.owner.running = False
    
    def render(self, display, offset):
        display.fill((0, 0, 0))

        text = ''
        for i, button in enumerate(self.buttons):
            text += f'> {button}\n' if i == self.selected_index else f'{button}\n'

        text_surf = Assets.FONT.render(text, antialias=False, color=(255, 255, 255))
        display.blit(text_surf, (16, 16))

    def get_input(self):
        just_pressed = pygame.key.get_just_pressed()

        # update input direction
        self.input_dir = pygame.Vector2(
            int(just_pressed[pygame.K_d]) - int(just_pressed[pygame.K_a]),
            int(just_pressed[pygame.K_s]) - int(just_pressed[pygame.K_w])
        )

        self.input_select = just_pressed[pygame.K_RETURN]
