from random import randint, choice
import pygame
from src.util import State, Assets
from .game_states import GameStates
from src.game.stars import StarSpawner

class Menu(State):
    def __init__(self):
        super().__init__(GameStates.MENU)

        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.input_dir = pygame.Vector2(0, 0)
        self.input_select = False 
        self.input_back = False 

        self.selected_page = 0
        self.selected_index = 0
        self.current_buttons: list[Button] = []

        self.pages = [
            [
                Button('Play', lambda: self.owner.state_machine.switch(GameStates.PLAYING)),
                Button('Settings', self._switch_to_settings), 
                Button('Quit', lambda: setattr(self.owner, 'running', False))
            ],
            [
                Button('Test', lambda: print('Test 1')),
                Button('Test 2', lambda: print('Test 2')),
                Button('Back', self._switch_to_main)
            ]
        ]

    def on_enter(self):
        self.star_spawner.spawn(30)
        self.owner.camera.boundary = None
        self.camera_movement = pygame.Vector2(
            choice([-1, 1]) * randint(25, 35), 
            choice([-1, 1]) * randint(10, 20)
        )
    
    def on_exit(self):
        self.star_spawner.clear()

    def update(self):
        self.owner.camera.set_render_callback(self.render)
        self.owner.camera.move_to(self.owner.camera.pos + self.camera_movement)

        self.get_input()

        self.current_buttons = self.pages[self.selected_page]
        self.selected_index = int((self.selected_index + self.input_dir.y) % len(self.current_buttons))

        if self.input_dir.y != 0:
            Assets.SOUNDS.play('blip')

        if self.input_select:
            Assets.SOUNDS.play('select')
            self.current_buttons[self.selected_index].select()
    
    def render(self, display, offset):
        display.fill(self.background_color)

        # display stars
        self.star_spawner.render(display, offset)

        # display menu
        text = ''
        for i, button in enumerate(self.current_buttons):
            text += f'> {button.text}\n' if i == self.selected_index else f'{button.text}\n'

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
    
    def _switch_to_settings(self):
        self.selected_page = 1
        self.selected_index = 0

    def _switch_to_main(self):
        self.selected_page = 0
        self.selected_index = 0


class Button():
    def __init__(self, text: str, callback: callable):
        self.text = text
        self.callback = callback
    
    def select(self):
        self.callback()

