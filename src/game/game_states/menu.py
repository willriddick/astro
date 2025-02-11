from random import randint, choice
import pygame
from src.util import State, Assets
from .game_states import GameStates
from src.game.stars import StarSpawner

class Menu(State):
    def __init__(self):
        super().__init__(GameStates.MENU)

        self.input_dir = pygame.Vector2(0, 0)
        self.input_select = False 
        self.input_back = False 

        self.buttons = ['Play', 'Settings', 'Quit']
        self.selected_index = 0

        self.star_spawner = StarSpawner()

        self.camera_movement: pygame.Vector2 = None
        self.background_color = (24, 20, 37)

    def on_enter(self):
        self.star_spawner.spawn(30, invert_depth=False)
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
        self.selected_index = (self.selected_index + self.input_dir.y) % len(self.buttons)
        if self.input_dir.y != 0:
            Assets.SOUNDS.play('select')

        if self.input_select:
            match self.selected_index:
                case 0:
                    self.owner.state_machine.switch(GameStates.PLAYING)
                case 1:
                    self.owner.state_machine.switch(GameStates.SETTINGS)
                case 2:
                    self.owner.running = False
    
    def render(self, display, offset):
        display.fill(self.background_color)

        # display stars
        self.star_spawner.render(display, offset)

        # display menu
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
