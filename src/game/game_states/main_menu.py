from random import randint, choice
import pygame
from src.util import State, Vec2
from src.game.menu import Menu, Button, ToggleButton, SliderButton
from src.game.entities import StarSpawner
from src.game.settings import Settings
from .game_states import GameStates

class MainMenu(State):
    def __init__(self):
        super().__init__(GameStates.MAIN_MENU)
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None
        self.settings = Settings()

        self.menu = Menu(
            pages = [
                [
                    Button('Play', self._play),
                    Button('Settings', self._switch_to_settings), 
                    Button('Quit', self._quit)
                ],
                [
                    ToggleButton('Fullscreen', lambda x: self.owner.set_fullscreen(x), self.settings.fullscreen),
                    SliderButton('Fuel UI Alpha', lambda x: self._set_fuel_ui_alpha(x), self.settings.fuel_ui_alpha),
                    SliderButton('Master Volume', lambda x: self._set_volume('master', x), self.settings.master_volume),
                    SliderButton('Sfx Volume', lambda x: self._set_volume('sfx', x), self.settings.sfx_volume),
                    SliderButton('Music Volume', lambda x: self._set_volume('music', x), self.settings.music_volume),
                    Button('Back', self._switch_to_main)
                ]
            ],
            position=Vec2(16, 180 - 16),
        )
    
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
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.star_spawner.render(display, offset)
        self.menu.render(display, offset)

    def _switch_to_settings(self):
        self.menu.change_page(1)

    def _switch_to_main(self):
        self.menu.change_page(0)
        self.settings.save()
    
    def _set_volume(self, type: str, value: int):
        if type == 'master':
            self.settings.master_volume = value
        elif type == 'sfx':
            self.settings.sfx_volume = value
        else:
            self.settings.music_volume = value
        self.settings.save()
    
    def _set_fuel_ui_alpha(self, value: int):
        self.settings.fuel_ui_alpha = value
    
    def _play(self):
        self.owner.state_machine.switch(GameStates.PLAYING)
    
    def _quit(self):
        self.owner.running = False
