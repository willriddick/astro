from random import randint, choice
import pygame
from src.util import State, Assets
from .game_states import GameStates
from src.game.entities import StarSpawner
from src.game.settings import Settings
from src.game.button import Button, ToggleButton, SliderButton

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
        self.hovered_index = 0
        self.current_buttons: list[Button] = []

        self.pages = [
            [
                Button('Play', self._play),
                Button('Settings', self._switch_to_settings), 
                Button('Quit', self._quit)
            ],
            [
                ToggleButton('Fullscreen', lambda x: self.owner.set_fullscreen(x), Settings.get_fullscreen()),
                SliderButton('Master Volume', lambda x: self._set_volume('master', x), Settings.get_master_volume()),
                SliderButton('Sfx Volume', lambda x: self._set_volume('sfx', x), Settings.get_sfx_volume()),
                SliderButton('Music Volume', lambda x: self._set_volume('music', x), Settings.get_music_volume()),
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
        self.hovered_index = int((self.hovered_index + self.input_dir.y) % len(self.current_buttons))

        if self.input_dir.y != 0:
            Assets.SOUNDS.play('blip')

        if self.input_select:
            self.current_buttons[self.hovered_index].select()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.star_spawner.render(display, offset)

        # display menu
        for index, button in enumerate(self.current_buttons):
            button.update(hovered=index == self.hovered_index)
            surface = button.get_surface()
            display.blit(surface, (16, 16 + self.current_buttons.index(button) * 16))

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
        self.hovered_index = 0
        Assets.SOUNDS.play('select')

    def _switch_to_main(self):
        self.selected_page = 0
        self.hovered_index = 0
        Settings.save()
        Assets.SOUNDS.play('select')
    
    def _set_volume(self, type: str, value: int):
        if type == 'master':
            Settings.set_master_volume(value)
        elif type == 'sfx':
            Settings.set_sfx_volume(value)
        else:
            Settings.set_music_volume(value)
        Assets.SOUNDS.play('blip', pitch_index=value)
    
    def _play(self):
        self.owner.state_machine.switch(GameStates.PLAYING)
        Assets.SOUNDS.play('select')
    
    def _quit(self):
        self.owner.running = False
        Assets.SOUNDS.play('select')
